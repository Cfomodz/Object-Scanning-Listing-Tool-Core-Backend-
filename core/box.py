from typing import List, Any, Optional
import qrcode
import os

class Box:
    """
    Generic container for multiple items (coins, cards, etc.).
    Can generate a QR code label representing the box and its contents.
    """
    def __init__(self, box_id: Optional[str] = None):
        self.items: List[Any] = []
        self.box_id: str = box_id or ""

    def add_item(self, item: Any) -> bool:
        if self.is_duplicate(item):
            print("Duplicate item detected.")
            return False
        self.items.append(item)
        return True

    def remove_last_item(self) -> Optional[Any]:
        if self.items:
            return self.items.pop()
        return None

    def is_duplicate(self, new_item: Any) -> bool:
        # Simple duplicate check by string representation
        return any(str(item) == str(new_item) for item in self.items)

    def total_value(self) -> float:
        return sum(getattr(item, 'price_guide_value', 0) for item in self.items)

    def to_dict(self) -> dict:
        return {
            'box_id': self.box_id,
            'items': [getattr(item, 'to_dict', lambda: dict(item))() for item in self.items],
            'total_value': self.total_value(),
        }

    def generate_qr_code(self, output_dir: str = 'tmp') -> str:
        """
        Generate a QR code image for the box (containing its ID or a URL).
        Returns the file path to the QR code image.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        qr_data = self.box_id or str(self.to_dict())
        img = qrcode.make(qr_data)
        qr_path = os.path.join(output_dir, f'box_qr_{self.box_id or "unknown"}.png')
        img.save(qr_path)
        return qr_path 