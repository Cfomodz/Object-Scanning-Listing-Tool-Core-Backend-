import pytest
from core.order import Order
from core.box import Box

def test_order_add_box():
    order = Order(target_value=1000.0)
    box = Box(box_id="testbox")
    # Simulate total_value method
    box.total_value = lambda: 200.0
    order.add_box(box)
    assert len(order.boxes) == 1
    assert order.remaining_value == 800.0 