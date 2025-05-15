from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ItemScanner(ABC):
    """
    Abstract base class for scanning and extracting data from images of an item.
    """
    @abstractmethod
    def scan(self, images: List[Any]) -> Dict[str, Any]:
        """
        Process a list of images and extract relevant data for the item.
        Args:
            images: List of image objects (format to be defined by implementation).
        Returns:
            Dictionary of extracted item data.
        """
        pass

class ListingBuilder(ABC):
    """
    Abstract base class for building a listing from scanned item data.
    """
    @abstractmethod
    def build_listing(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a listing (e.g., JSON or API payload) from item data.
        Args:
            item_data: Dictionary of extracted item data.
        Returns:
            Dictionary representing the listing.
        """
        pass 