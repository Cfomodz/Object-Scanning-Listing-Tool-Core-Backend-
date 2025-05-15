import pytest
from core.box import Box
from plugins.coin.coin import Coin

def test_box_add_coin():
    box = Box(box_id="testbox")
    coin_data = {"PCGSNo": "12345", "CertNo": "67890", "Barcode": "1111222233334444", "Name": "Test Coin", "Year": 2020, "Denomination": "25C", "PriceGuideValue": 100.0}
    coin = Coin(coin_data)
    result = box.add_item(coin)
    assert result is True or result is None  # Depending on add_item logic
    assert len(box.items) == 1 