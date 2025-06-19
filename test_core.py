import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import io

# Import core modules
from core.barcode_scanner import BarcodeScanner, images_are_similar
from core.environment_setup import load_core_env, PluginRegistry
from core.label_writer import LabelWriter
from core.listing import Listing, process_images_to_listings


class TestBarcodeScanner(unittest.TestCase):
    """Test cases for BarcodeScanner class."""
    
    def setUp(self):
        self.scanner = BarcodeScanner()
        # Create test image
        self.test_image = Image.new('RGB', (100, 100), color='white')
    
    def test_scan_image_for_barcode_returns_none_for_no_barcode(self):
        """Test that scanning an image with no barcode returns None."""
        result = BarcodeScanner.scan_image_for_barcode(self.test_image)
        self.assertIsNone(result)
    
    @patch('core.barcode_scanner.decode')
    def test_scan_image_for_barcode_returns_decoded_string(self, mock_decode):
        """Test that scanning an image with barcode returns decoded string."""
        mock_barcode = Mock()
        mock_barcode.data.decode.return_value = "test_barcode_123"
        mock_decode.return_value = [mock_barcode]
        
        result = BarcodeScanner.scan_image_for_barcode(self.test_image)
        self.assertEqual(result, "test_barcode_123")
    
    def test_process_frame_returns_barcode_string(self):
        """Test that process_frame returns barcode string when found."""
        with patch.object(self.scanner, 'scan_image_for_barcode', return_value="test_123") as mock_scan:
            result = self.scanner.process_frame(self.test_image)
            self.assertEqual(result, "test_123")
            mock_scan.assert_called_once_with(self.test_image)
    
    def test_process_frame_returns_none_when_no_barcode(self):
        """Test that process_frame returns None when no barcode found."""
        with patch.object(self.scanner, 'scan_image_for_barcode', return_value=None) as mock_scan:
            result = self.scanner.process_frame(self.test_image)
            self.assertIsNone(result)
    
    @patch('core.barcode_scanner.os.makedirs')
    @patch('core.barcode_scanner.json.dump')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_json_creates_logs_directory(self, mock_open, mock_json_dump, mock_makedirs):
        """Test that save_json creates logs directory if it doesn't exist."""
        with patch('core.barcode_scanner.os.path.exists', return_value=False):
            BarcodeScanner.save_json('test.json', {'key': 'value'})
            mock_makedirs.assert_called_once_with('logs')
    
    @patch('core.barcode_scanner.json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_load_json_loads_from_logs_directory(self, mock_open, mock_json_load):
        """Test that load_json loads from the logs directory."""
        mock_json_load.return_value = {'test': 'data'}
        result = BarcodeScanner.load_json('test.json')
        mock_open.assert_called_once_with('logs/test.json', 'r')
        self.assertEqual(result, {'test': 'data'})




class TestImagesAreSimilar(unittest.TestCase):
    """Test cases for images_are_similar function."""
    
    def setUp(self):
        self.img1 = Image.new('RGB', (100, 100), color='red')
        self.img2 = Image.new('RGB', (100, 100), color='red')
        self.img3 = Image.new('RGB', (100, 100), color='blue')
    
    def test_identical_images_are_similar(self):
        """Test that identical images are considered similar."""
        result = images_are_similar(self.img1, self.img2)
        self.assertTrue(result)
    
    def test_different_images_are_not_similar(self):
        """Test that completely different images are not similar."""
        result = images_are_similar(self.img1, self.img3, threshold=0.1)
        self.assertFalse(result)
    
    def test_threshold_affects_similarity(self):
        """Test that threshold parameter affects similarity determination."""
        # Same images should be similar regardless of threshold
        result_low = images_are_similar(self.img1, self.img2, threshold=0.1)
        result_high = images_are_similar(self.img1, self.img2, threshold=0.9)
        self.assertTrue(result_low)
        self.assertTrue(result_high)


class TestEnvironmentSetup(unittest.TestCase):
    """Test cases for environment setup functionality."""
    
    @patch('core.environment_setup.load_dotenv')
    @patch('core.environment_setup.os.path.abspath')
    @patch('core.environment_setup.os.path.join')
    def test_load_core_env_loads_dotenv(self, mock_join, mock_abspath, mock_load_dotenv):
        """Test that load_core_env loads the .env file."""
        mock_abspath.return_value = '/test/path'
        mock_join.side_effect = ['/test/path', '/test/path/.env']
        
        load_core_env()
        
        mock_load_dotenv.assert_called_once_with(dotenv_path='/test/path/.env')


class TestPluginRegistry(unittest.TestCase):
    """Test cases for PluginRegistry class."""
    
    def setUp(self):
        # Clear registry before each test
        PluginRegistry._scanners = {}
        PluginRegistry._builders = {}
    
    def test_register_scanner(self):
        """Test scanner registration."""
        mock_scanner = Mock()
        PluginRegistry.register_scanner('test_type', mock_scanner)
        self.assertEqual(PluginRegistry._scanners['test_type'], mock_scanner)
    
    def test_register_builder(self):
        """Test builder registration."""
        mock_builder = Mock()
        PluginRegistry.register_builder('test_type', mock_builder)
        self.assertEqual(PluginRegistry._builders['test_type'], mock_builder)
    
    def test_get_scanner(self):
        """Test getting registered scanner."""
        mock_scanner = Mock()
        PluginRegistry._scanners['test_type'] = mock_scanner
        result = PluginRegistry.get_scanner('test_type')
        self.assertEqual(result, mock_scanner)
    
    def test_get_builder(self):
        """Test getting registered builder."""
        mock_builder = Mock()
        PluginRegistry._builders['test_type'] = mock_builder
        result = PluginRegistry.get_builder('test_type')
        self.assertEqual(result, mock_builder)
    
    def test_available_types(self):
        """Test getting available types."""
        mock_scanner = Mock()
        mock_builder = Mock()
        PluginRegistry._scanners['type1'] = mock_scanner
        PluginRegistry._builders['type1'] = mock_builder
        PluginRegistry._scanners['type2'] = mock_scanner
        
        result = PluginRegistry.available_types()
        
        expected = {
            'type1': {'scanner': mock_scanner, 'builder': mock_builder},
            'type2': {'scanner': mock_scanner, 'builder': None}
        }
        self.assertEqual(result, expected)


class TestLabelWriter(unittest.TestCase):
    """Test cases for LabelWriter class."""
    
    def setUp(self):
        # Create concrete implementation for testing
        class TestLabelWriter(LabelWriter):
            def create_label_content(self, item):
                return f"Label for {item}"
            
            def create_label_document(self, item, **kwargs):
                return f"document_for_{item}.pdf"
        
        self.label_writer = TestLabelWriter()
    
    @patch('core.label_writer.barcode.get')
    def test_create_barcode_generates_barcode(self, mock_barcode_get):
        """Test that create_barcode generates a barcode image."""
        mock_barcode_instance = Mock()
        mock_barcode_get.return_value = mock_barcode_instance
        
        result = LabelWriter.create_barcode("test_data_123")
        
        mock_barcode_get.assert_called_once()
        mock_barcode_instance.save.assert_called_once_with("barcode_test_data_123")
        self.assertEqual(result, "barcode_test_data_123.png")
    
    def test_create_label_content_abstract_method(self):
        """Test that create_label_content works in concrete implementation."""
        result = self.label_writer.create_label_content("test_item")
        self.assertEqual(result, "Label for test_item")
    
    def test_create_label_document_abstract_method(self):
        """Test that create_label_document works in concrete implementation."""
        result = self.label_writer.create_label_document("test_item")
        self.assertEqual(result, "document_for_test_item.pdf")
    
    @patch('core.label_writer.os.path.exists', return_value=False)
    def test_print_label_file_not_found(self, mock_exists):
        """Test print_label when file doesn't exist."""
        with patch('builtins.print') as mock_print:
            self.label_writer.print_label("nonexistent.pdf", "test_printer")
            mock_print.assert_called_with("File not found: /home/toor/Object-Scanning-Listing-Tool-Core-Backend-/nonexistent.pdf")


class TestListing(unittest.TestCase):
    """Test cases for Listing class."""
    
    def setUp(self):
        self.mock_scanner = Mock()
        self.test_images = [Image.new('RGB', (100, 100), color='red')]
    
    def test_listing_requires_barcode_scanner(self):
        """Test that Listing requires a BarcodeScanner instance."""
        with self.assertRaises(ValueError):
            Listing()
    
    def test_listing_initialization_with_item(self):
        """Test Listing initialization with provided item."""
        test_item = {'name': 'test_item'}
        listing = Listing(item=test_item, barcode_scanner=self.mock_scanner)
        self.assertEqual(listing.item, test_item)
    
    def test_listing_initialization_with_images(self):
        """Test Listing initialization with images (tries to find item)."""
        self.mock_scanner.process_frame.return_value = {'found': 'item'}
        
        listing = Listing(images=self.test_images, barcode_scanner=self.mock_scanner)
        
        self.mock_scanner.process_frame.assert_called_with(self.test_images[0], return_coin=True)
        self.assertEqual(listing.item, {'found': 'item'})
    
    def test_listing_to_dict(self):
        """Test that to_dict returns proper dictionary representation."""
        test_item = Mock()
        test_item.__dict__ = {'name': 'test', 'value': 100}
        
        listing = Listing(
            item=test_item, 
            price_paid=50.0, 
            listing_price=75.0,
            images=['img1.jpg'],
            barcode_scanner=self.mock_scanner
        )
        
        result = listing.to_dict()
        expected = {
            'item': {'name': 'test', 'value': 100},
            'price_paid': 50.0,
            'listing_price': 75.0,
            'images': ['img1.jpg']
        }
        self.assertEqual(result, expected)


class TestProcessImagesToListings(unittest.TestCase):
    """Test cases for process_images_to_listings function."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create test images
        for i in range(5):
            img = Image.new('RGB', (100, 100), color='red' if i == 0 else 'blue')
            img.save(os.path.join(self.temp_dir, f'image_{i}.jpg'))
    
    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_process_images_to_listings_basic(self):
        """Test basic image grouping functionality."""
        result = process_images_to_listings(self.temp_dir, 2, "n")
        
        # Should have 3 groups: [img1, img2], [img3, img4], [img5]
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[1]), 2)
        self.assertEqual(len(result[2]), 1)
    
    @patch('core.listing.images_are_similar')
    def test_process_images_skips_blank_images(self, mock_similar):
        """Test that blank images are skipped."""
        # First image is blank, second image is similar to blank
        mock_similar.side_effect = [False, True, False, False, False]
        
        result = process_images_to_listings(self.temp_dir, 2, "y")
        
        # Should skip first image as blank and second as similar to blank
        # Result should have fewer images
        self.assertLess(len(result), 3)


if __name__ == '__main__':
    unittest.main() 