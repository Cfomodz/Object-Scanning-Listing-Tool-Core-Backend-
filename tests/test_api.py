import io
import pytest
from PIL import Image
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def create_test_image():
    img = Image.new('RGB', (100, 100), color='white')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_barcode_read(client):
    img_bytes = create_test_image()
    data = {'image': (img_bytes, 'test.jpg')}
    response = client.post('/barcode/read', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'barcode' in response.get_json()

def test_visual_match(client):
    img_bytes = create_test_image()
    data = {'image': (img_bytes, 'test.jpg')}
    response = client.post('/visual/match', data=data, content_type='multipart/form-data')
    assert response.status_code == 501
    assert 'result' in response.get_json()

def test_listing_from_images(client):
    img1 = create_test_image()
    img2 = create_test_image()
    data = {
        'images': [
            (img1, 'img1.jpg'),
            (img2, 'img2.jpg')
        ]
    }
    response = client.post('/listing/from-images', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'item' in response.get_json()

def test_decision_image(client):
    img_bytes = create_test_image()
    data = {
        'image': (img_bytes, 'test.jpg'),
        'threshold': '0.7'
    }
    response = client.post('/decision/image', data=data, content_type='multipart/form-data')
    assert response.status_code == 501
    assert 'result' in response.get_json()

def test_decision_barcode(client):
    response = client.post('/decision/barcode', json={'barcode': '1234567890', 'threshold': 0.7})
    assert response.status_code == 501
    assert 'result' in response.get_json()

def test_box_create(client):
    response = client.post('/box/create', json={'barcodes': ['123', '456']})
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total_value' in data

def test_order_create(client):
    response = client.post('/order/create', json={'barcodes': ['123', '456'], 'target_value': 1000})
    assert response.status_code == 200
    data = response.get_json()
    assert 'target_value' in data
    assert 'remaining_value' in data
    assert 'boxes' in data 