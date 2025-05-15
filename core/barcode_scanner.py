import time
from PIL import Image
from pyzbar.pyzbar import decode
from typing import Optional, Any
import os
import json

class BarcodeScanner:
    """
    Core service for barcode extraction from images.
    Used by all item plugins for identification.
    Provides static methods for JSON cache I/O in the logs directory.
    """
    @staticmethod
    def scan_image_for_barcode(image: Any) -> Optional[str]:
        """
        Decode a barcode from an image (file path or PIL Image).
        Returns the decoded string (cert number) or None.
        """
        if isinstance(image, str):
            image = Image.open(image)
        grayscale_image = image.convert('L')
        barcodes = decode(grayscale_image)
        if barcodes:
            return barcodes[0].data.decode('utf-8')
        return None

    def process_frame(self, image: Any, return_coin: bool = False) -> Optional[Any]:
        """
        Scan an image for a barcode and return the barcode string if found.
        If return_coin is True, this method should be overridden by plugins to return an item object.
        """
        barcode = self.scan_image_for_barcode(image)
        if barcode:
            return barcode
        return None

    @staticmethod
    def load_json(path: str) -> Any:
        """
        Load JSON data from a file in the logs directory.
        """
        full_path = os.path.join('logs', path)
        with open(full_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_json(path: str, data: Any) -> None:
        """
        Save data as JSON to a file in the logs directory.
        """
        if not os.path.exists('logs'):
            os.makedirs('logs')
        full_path = os.path.join('logs', path)
        with open(full_path, 'w') as f:
            json.dump(data, f)

    def identify_product(self, image: Any) -> Optional[Any]:
        """
        Identify a product (e.g., coin) from an image by barcode or visual means.
        Returns the product object or None if not found.
        """
        barcode = self.scan_image_for_barcode(image)
        if barcode:
            grading_service = "PCGS" if len(barcode) == 16 else "NGC"
            return self.api.make_api_call(barcode, grading_service)
        # TODO: Add visual identification fallback here
        return None 