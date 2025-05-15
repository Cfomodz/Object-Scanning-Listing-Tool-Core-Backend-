from PIL import Image, ImageChops

def images_are_similar(img1: Image.Image, img2: Image.Image, threshold: float = 0.65) -> bool:
    """Return True if images are similar below a threshold."""
    diff = ImageChops.difference(img1, img2)
    bbox = diff.getbbox()
    if not bbox:
        return True  # Images are identical
    diff_percentage = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) / (img1.size[0] * img1.size[1])
    return diff_percentage < threshold 