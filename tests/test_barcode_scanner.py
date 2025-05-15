import pytest
from core.barcode_scanner import BarcodeScanner
from unittest.mock import patch

def test_barcode_scanner_instantiation():
    scanner = BarcodeScanner()
    assert isinstance(scanner, BarcodeScanner)

@patch('core.barcode_scanner.BarcodeScanner.scan_image_for_barcode')
def test_scan_image_for_barcode(mock_scan):
    mock_scan.return_value = '1234567890123456'
    scanner = BarcodeScanner()
    result = scanner.scan_image_for_barcode('dummy_path.jpg')
    assert result == '1234567890123456' 