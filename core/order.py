from typing import Optional, List
from core.box import Box
from core.barcode_scanner import BarcodeScanner

class Order:
    """
    A collection of boxes for a target value order (generic, not coin-specific).
    """
    def __init__(self, target_value: float):
        self.boxes: List[Box] = []
        self.target_value: float = target_value
        self.remaining_value: float = target_value

    def add_box(self, box: Box) -> None:
        self.boxes.append(box)
        self.remaining_value -= box.total_value()

    def is_duplicate(self, new_item) -> bool:
        for box in self.boxes:
            if box.is_duplicate(new_item):
                return True
        return False

    def save_to_file(self, path: str = "order.json") -> None:
        order_data = {
            "target_value": self.target_value,
            "remaining_value": self.remaining_value,
            "boxes": [box.box_id for box in self.boxes]
        }
        BarcodeScanner.save_json(path, order_data)
        print(f"Order saved to {path}")

    @classmethod
    def load_from_file(cls, path: str = "order.json") -> Optional['Order']:
        try:
            order_data = BarcodeScanner.load_json(path)
            order = cls(order_data["target_value"])
            order.remaining_value = order_data["remaining_value"]
            # Box loading by ID is left to the application
            return order
        except FileNotFoundError:
            print("No order found")
            return None

    def __str__(self) -> str:
        return f"Order with {len(self.boxes)} boxes, target value: ${self.target_value:.2f}, remaining value: ${self.remaining_value:.2f}" 