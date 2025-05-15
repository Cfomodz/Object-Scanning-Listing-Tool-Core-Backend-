import os
from PIL import Image
from typing import List
from core.image_utils import images_are_similar

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