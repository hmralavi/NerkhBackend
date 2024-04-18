import unittest
import sys

sys.path.append("src")

from data_tools import quantize_datetime, is_prices_same_day, PriceData
from datetime import datetime, timezone, timedelta


class TestDateTools(unittest.TestCase):

    def test_quantize_datetime(self):
        """
        a test to convert datetime to float number. e.g: 10:30:35 --> 10.5, 00:23:00 --> 0.25
        """
        dt = datetime(year=2024, month=2, day=15, hour=10, minute=0, second=0, microsecond=250, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt), 10.0)

        dt = datetime(year=2024, month=2, day=15, hour=0, minute=59, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt), 0.75)

        dt = datetime(year=2024, month=2, day=15, hour=23, minute=59, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt), 23.75)

        dt = datetime(year=2024, month=2, day=15, hour=0, minute=0, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt), 0.0)

        dt = datetime(year=2024, month=2, day=15, hour=10, minute=15, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt), 10.25)

        dt = datetime(year=2024, month=2, day=15, hour=10, minute=10, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt), 10.0)

        dt = datetime(year=2024, month=2, day=15, hour=10, minute=25, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt, quantize_level=0.5), 10.0)

        dt = datetime(year=2024, month=2, day=15, hour=10, minute=40, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt, quantize_level=0.5), 10.5)

        dt = datetime(year=2024, month=2, day=15, hour=16, minute=30, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt, quantize_level=1), 16.0)

        dt = datetime(year=2024, month=2, day=15, hour=16, minute=30, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt, quantize_level=2), 16.0)

        dt = datetime(year=2024, month=2, day=15, hour=16, minute=30, second=59, microsecond=0, tzinfo=timezone.utc)
        self.assertEqual(quantize_datetime(dt, quantize_level=3), 15.0)

    def test_is_prices_same_day(self):
        """
        test if the two prices belong to the same day
        """
        d = datetime.fromisoformat("2024-05-02T15:00:00")
        p1 = PriceData(time=(d - timedelta(hours=3)).isoformat())
        p2 = PriceData(time=d.isoformat())
        self.assertTrue(is_prices_same_day(p1, p2))

        d = datetime.fromisoformat("2024-05-02T02:00:00")
        p1 = PriceData(time=(d - timedelta(hours=3)).isoformat())
        p2 = PriceData(time=d.isoformat())
        self.assertFalse(is_prices_same_day(p1, p2))

        d = datetime.fromisoformat("2024-05-02T21:00:00")
        p1 = PriceData(time=(d + timedelta(hours=3)).isoformat())
        p2 = PriceData(time=d.isoformat())
        self.assertFalse(is_prices_same_day(p1, p2))

        d = datetime.fromisoformat("2024-05-02T01:00:00")
        p1 = PriceData(time=(d - timedelta(hours=1, minutes=1)).isoformat())
        p2 = PriceData(time=d.isoformat())
        self.assertFalse(is_prices_same_day(p1, p2))


if __name__ == "__main__":
    unittest.main()
