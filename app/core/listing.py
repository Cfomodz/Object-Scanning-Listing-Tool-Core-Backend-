from typing import Any, Optional, List
import os
from PIL import Image
from core.barcode_scanner import images_are_similar

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

def process_images_to_listings(dir_of_slab_images: str, images_per_listing: int, first_image_is_blank: str = "n") -> List[List[str]]:
    """Groups images into listings, skipping blanks. Returns list of image path groups."""
    blank_image = None
    listings = []
    current_listing_images = []

    for index, image_name in enumerate(os.listdir(dir_of_slab_images)):
        image_path = os.path.join(dir_of_slab_images, image_name)
        image = Image.open(image_path)

        if blank_image is None and first_image_is_blank.lower() == "y":
            blank_image = image
            continue

        if blank_image and images_are_similar(image, blank_image):
            continue

        current_listing_images.append(image_path)

        if len(current_listing_images) == images_per_listing:
            listings.append(list(current_listing_images))
            current_listing_images = []

    if current_listing_images:
        listings.append(list(current_listing_images))
    return listings 