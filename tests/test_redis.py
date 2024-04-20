import unittest
from settings import *
import redis
from datetime import datetime, timedelta
import json
import sys

sys.path.append("src")

from data_tools import PriceData
from app import store_price_in_db, get_price_from_db, analyze_and_store_price


class TestRedisConnection(unittest.TestCase):

    def test_redis_connection(self):
        """
        test if connection to redis database is successfull.
        """
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_INDEX)
            r.ping()  # Test if the connection is working by sending a PING command
            connected = True
        except redis.ConnectionError:
            connected = False
        self.assertTrue(connected, "Failed to connect to Redis database")


class TestRedisData(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_INDEX)
        r.flushdb()
        cls.r = r

    @classmethod
    def tearDownClass(cls) -> None:
        cls.r.flushdb()

    def setUp(self) -> None:
        self.r.flushdb()

    def test_string(self):
        """
        insert a string key&value and check if they are stored correctly.
        """
        key = "testkey1"
        value = "testvalue1"
        self.r.set(key, value)
        self.assertTrue(self.r.exists(key))
        self.assertEqual(self.r.get(key).decode("utf-8"), value)

    def test_int(self):
        """
        insert a int key&value and check if they are stored correctly.
        """
        key = 132
        value = 123
        self.r.set(key, value)
        self.assertTrue(self.r.exists(key))
        self.assertEqual(int(self.r.get(key)), value)

    def test_datetime(self):
        """
        insert a datetime key&value and check if they are stored correctly.
        """
        key = datetime(2024, 1, 5, 23, 45, 0)
        value = datetime(2024, 1, 6, 23, 45, 0)
        self.r.set(key.isoformat(), value.isoformat())
        self.assertTrue(self.r.exists(key.isoformat()))
        self.assertEqual(datetime.fromisoformat(self.r.get(key.isoformat()).decode("utf-8")), value)

    def test_json(self):
        """
        insert a json value and check if they are stored correctly.
        """
        my_dict = {"key1": "value1", "key2": "value2", "key3": 3}
        json_str = json.dumps(my_dict)
        self.r.set("my_dict_key", json_str)
        stored_json_str = self.r.get("my_dict_key")
        stored_dict = json.loads(stored_json_str)
        self.assertEqual(my_dict, stored_dict)

    def test_2d_index(self):
        name = "USD"
        time = "10.25"
        price = "14700"
        key = f"variable:{name}:{time}"
        self.r.hset(key, "value", price)
        self.assertEqual(self.r.hget(key, "value").decode("utf-8"), price)

    def test_store_get_price_from_db(self):
        p = PriceData(
            code="USD",
            name="us dollar",
            source="bonbast",
            price_sell=70000,
            price_buy=68000,
            time=datetime.now().isoformat(),
        )
        store_price_in_db(p.code, p, self.r)
        self.assertEqual(p.model_dump(), get_price_from_db(p.code, self.r).model_dump())

    def test_analyze_and_store(self):
        # try to insert a price with invalid code, expected to get an error
        newprice = PriceData(code="fake")
        with self.assertRaises(KeyError):
            analyze_and_store_price(newprice, self.r)

        # insert a valid code and retrieve it
        code = "USD-TMN"
        newprice = PriceData(code=code, price_sell=70000, price_buy=69000, time="2024-05-02T17:15:00")
        analyze_and_store_price(newprice, self.r)
        self.assertEqual(newprice.model_dump(), get_price_from_db(f"{code}:current", self.r).model_dump())

        # insert a valid code while it is already available in the db (same day, 15 mins later)
        newprice = PriceData(code=code, price_sell=72000, price_buy=70000, time="2024-05-02T17:30:00")
        analyze_and_store_price(newprice, self.r)
        self.assertFalse(self.r.exists(f"{code}:yesterday"))  # we shouldn't still have a price for yesterday
        self.assertEqual(newprice.model_dump(), get_price_from_db(f"{code}:current", self.r).model_dump())

        # insert a valid code while it is already available in the db (next day)
        newprice_newday = PriceData(code=code, price_sell=75000, price_buy=74000, time="2024-05-03T17:30:00")
        analyze_and_store_price(newprice_newday, self.r)
        self.assertTrue(self.r.exists(f"{code}:yesterday"))  # we should have a price for yesterday
        self.assertEqual(newprice.model_dump(), get_price_from_db(f"{code}:yesterday", self.r).model_dump())

        current_price = get_price_from_db(f"{code}:current", self.r)
        self.assertNotEqual(newprice_newday.model_dump(), current_price.model_dump())
        self.assertEqual(current_price.price_sell_change, 3000)
        self.assertEqual(current_price.price_buy_change, 4000)


if __name__ == "__main__":
    unittest.main()
