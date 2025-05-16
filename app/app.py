# main.py (refactored for plugin-based architecture)
from .core.environment_setup import load_core_env, PluginRegistry
from .core.barcode_scanner import BarcodeScanner, images_are_similar
from .core.listing import Listing
from flask import Flask, request, jsonify
from PIL import Image
import io
import sys
import os

# Load core environment variables
load_core_env()

app = Flask(__name__)

@app.route('/barcode/read', methods=['POST'])
def barcode_read():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    image_file = request.files['image']
    image = Image.open(image_file.stream)
    barcode = BarcodeScanner.scan_image_for_barcode(image)
    return jsonify({'barcode': barcode})

@app.route('/visual/match', methods=['POST'])
def visual_match():
    # Stub: Visual match logic would require plugin or model
    return jsonify({'result': 'Visual match not implemented'}), 501

@app.route('/listing/from-images', methods=['POST'])
def listing_from_images():
    images = request.files.getlist('images')
    if not images:
        return jsonify({'error': 'No images uploaded'}), 400
    pil_images = [Image.open(img.stream) for img in images]
    # Use barcode scanner for now; plugin logic can be added
    scanner = BarcodeScanner()
    listing = Listing(images=[img for img in pil_images], barcode_scanner=scanner)
    return jsonify(listing.to_dict())

@app.route('/decision/image', methods=['POST'])
def decision_image():
    if 'image' not in request.files or 'threshold' not in request.form:
        return jsonify({'error': 'Image and threshold required'}), 400
    image_file = request.files['image']
    threshold = float(request.form['threshold'])
    # For demo: compare to a reference image (not provided)
    # In real use, reference image should be provided or loaded
    return jsonify({'result': 'Not implemented: need reference image for comparison'}), 501

@app.route('/decision/barcode', methods=['POST'])
def decision_barcode():
    data = request.get_json()
    barcode = data.get('barcode')
    threshold = data.get('threshold')
    # For demo: logic to decide keep/toss based on barcode
    # In real use, implement business logic here
    return jsonify({'result': 'Not implemented: need business logic for barcode decision'}), 501

def main():
    if 'flask' in sys.argv or os.environ.get('FLASK_APP'):
        app.run(debug=True, host='0.0.0.0', port=5000)
        return
    if len(sys.argv) < 2:
        print("Usage: python app.py <item_type> [args...]")
        sys.exit(1)
    item_type = sys.argv[1]
    plugin = PluginRegistry.available_types().get(item_type)
    if not plugin:
        print(f"No plugin registered for type '{item_type}'")
        sys.exit(1)
    # Further CLI logic would go here (e.g., process images, create listings, etc.)
    print(f"Plugin for '{item_type}' loaded: {plugin}")

if __name__ == "__main__":
    main()
