import unittest
from unittest.mock import patch, MagicMock
import os

from .core.listing import Listing
from .core.barcode_scanner import BarcodeScanner

# --- Listing Tests ---
class DummyCoin:
    def __init__(self):
        self.PCGSNo = "12345"
        self.CertNo = "67890"
        self.Barcode = "1111222233334444"
        self.Name = "Test Coin"
        self.Year = 2020
        self.Denomination = "25C"
        self.price_guide_value = 100.0
    def __str__(self):
        return f"{self.PCGSNo}-{self.CertNo}"

class ListingTestCase(unittest.TestCase):
    def test_listing_instantiation(self):
        images = ["barcode.jpg", "front.jpg", "back.jpg"]
        call_results = [DummyCoin(), None, None]
        def mock_process_frame(image, return_coin=False):
            result = call_results.pop(0) if call_results else None
            if return_coin:
                return result
            return result is not None
        scanner = BarcodeScanner()
        with patch.object(scanner, 'process_frame', new=mock_process_frame):
            listing = Listing(item=None, price_paid=50.0, listing_price=100.0, images=images, barcode_scanner=scanner)
            self.assertEqual(listing.price_paid, 50.0)
            self.assertEqual(listing.listing_price, 100.0)
            self.assertEqual(listing.images, images)
            self.assertIsNotNone(listing.item)
            self.assertEqual(listing.item.Name, "Test Coin")
            self.assertEqual(listing.item.PCGSNo, "12345")

# --- BarcodeScanner Tests ---
class BarcodeScannerTestCase(unittest.TestCase):
    def test_barcode_scanner_instantiation(self):
        scanner = BarcodeScanner()
        self.assertIsInstance(scanner, BarcodeScanner)

    @patch('core.barcode_scanner.BarcodeScanner.scan_image_for_barcode')
    def test_scan_image_for_barcode(self, mock_scan):
        mock_scan.return_value = '1234567890123456'
        scanner = BarcodeScanner()
        result = scanner.scan_image_for_barcode('dummy_path.jpg')
        self.assertEqual(result, '1234567890123456')

# --- Plugin Discovery Test ---
class PluginDiscoveryTestCase(unittest.TestCase):
    def test_plugin_tests_run(self):
        plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        if not os.path.isdir(plugins_dir):
            self.skipTest("No plugins directory found.")
        for plugin_name in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, plugin_name)
            tests_path = os.path.join(plugin_path, 'tests')
            if os.path.isdir(tests_path):
                for fname in os.listdir(tests_path):
                    if fname.startswith('test_') and fname.endswith('.py'):
                        # Just check import does not fail
                        mod_name = f'plugins.{plugin_name}.tests.{fname[:-3]}'
                        try:
                            __import__(mod_name)
                        except Exception as e:
                            self.fail(f"Failed to import {mod_name}: {e}")

if __name__ == "__main__":
    unittest.main()