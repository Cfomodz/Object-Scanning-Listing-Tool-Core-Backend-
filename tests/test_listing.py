import pytest
from core.listing import Listing
from core.barcode_scanner import BarcodeScanner
from unittest.mock import patch
import os

class DummyCoin:
    def __init__(self):
        self.name = "Test Coin"
        self.sku = "123456"
        self.__dict__ = {"name": "Test Coin", "sku": "123456"}

def get_images_from_dir(directory):
    if not os.path.isdir(directory):
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

def test_listing_instantiation():
    images = ["barcode.jpg", "front.jpg", "back.jpg"]
    # Simulate: first image has barcode, others do not
    call_results = [DummyCoin(), None, None]
    def mock_process_frame(image, return_coin=False):
        result = call_results.pop(0) if call_results else None
        if return_coin:
            return result
        return result is not None

    scanner = BarcodeScanner()
    with patch.object(scanner, 'process_frame', new=mock_process_frame):
        listing = Listing(item=None, price_paid=50.0, listing_price=100.0, images=images, barcode_scanner=scanner)
        assert listing.price_paid == 50.0
        assert listing.listing_price == 100.0
        assert listing.images == images
        assert listing.item is not None
        assert listing.item.name == "Test Coin"
        assert listing.item.sku == "123456" 