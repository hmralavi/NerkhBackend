import unittest
from settings import *
import redis
from datetime import datetime
import json


class TestRedisConnection(unittest.TestCase):

    def test_redis_connection(self):
        """
        test if connection to redis database is successfull.
        """
        try:
            r = redis.Redis(host=DATABASE_HOST, port=DATABASE_PORT, db=DATABASE_INDEX)
            r.ping()  # Test if the connection is working by sending a PING command
            connected = True
        except redis.ConnectionError:
            connected = False
        self.assertTrue(connected, "Failed to connect to Redis database")


class TestRedisData(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        r = redis.Redis(host=DATABASE_HOST, port=DATABASE_PORT, db=DATABASE_INDEX)
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
        self.assertDictEqual(my_dict, stored_dict)


if __name__ == "__main__":
    unittest.main()
