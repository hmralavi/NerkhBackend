import unittest
import sys

sys.path.append("src")

from data_tools import (
    quantize_datetime,
    is_prices_same_day,
    PriceData,
    MAIN_CODES,
    bonbast_translate_dict,
    iranjib_transtale_dict,
    translate_prices,
)
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


class TestTranslator(unittest.TestCase):
    def test_bonbast_dict(self):
        """
        check if all values in the dict is available in the MAIN_CODES
        """
        for k in bonbast_translate_dict.keys():
            self.assertTrue(
                bonbast_translate_dict[k] in MAIN_CODES,
                f"bonbast_translate_dict value {bonbast_translate_dict[k]} not in the MAIN_CODES.",
            )

    def test_iranjib_dict(self):
        """
        check if all values in the dict is available in the MAIN_CODES
        """
        for k in iranjib_transtale_dict.keys():
            self.assertTrue(
                iranjib_transtale_dict[k] in MAIN_CODES,
                f"iranjib_translate_dict value {iranjib_transtale_dict[k]} not in the MAIN_CODES.",
            )

    def test_transtalte_prices_func(self):
        """
        testing the transtale_prices function.
        """
        prices = [
            PriceData(code="USD___", source="bonbast", price1=1),
            PriceData(code="USD", source="bonbast", price1=2),
            PriceData(code="USD", source="bonbast___", price1=3),
        ]
        translated = translate_prices(prices=prices, prune=True)
        self.assertEqual(len(translated), 1)
        self.assertEqual(translated[0].price1, 2)
        self.assertEqual(translated[0].code, "USD-TMN")

        translated_no_prune = translate_prices(prices=prices, prune=False)
        self.assertEqual(len(translated_no_prune), 3)
        self.assertEqual(translated_no_prune[0].price1, 1)
        self.assertEqual(translated_no_prune[2].price1, 3)
        self.assertEqual(translated_no_prune[0].code, "USD___")
        self.assertEqual(translated_no_prune[2].source, "bonbast___")


if __name__ == "__main__":
    unittest.main()
