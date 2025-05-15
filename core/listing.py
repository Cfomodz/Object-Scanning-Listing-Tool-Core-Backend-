from typing import Any, Optional, List

class Listing:
    """
    Generic listing for an item, constructed from images and barcode scanning.
    """
    def __init__(self, item: Optional[Any] = None, price_paid: Optional[float] = None, listing_price: Optional[float] = None, images: Optional[List[str]] = None, barcode_scanner: Any = None):
        if barcode_scanner is None:
            raise ValueError("A BarcodeScanner instance must be provided to Listing.")
        self.item: Optional[Any] = item
        self.price_paid: Optional[float] = price_paid
        self.listing_price: Optional[float] = listing_price
        self.images: List[str] = images if images is not None else []
        self.BarcodeScanner = barcode_scanner

        if self.item is None and self.images:
            for image in self.images:
                # The test expects process_frame(image, return_coin=True)
                coin = self.BarcodeScanner.process_frame(image, return_coin=True)
                if coin:
                    self.item = coin
                    break

    def to_dict(self) -> dict:
        return {
            "item": getattr(self.item, '__dict__', self.item),
            "price_paid": self.price_paid,
            "listing_price": self.listing_price,
            "images": self.images
        } 