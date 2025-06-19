import unittest
import json
import io
from unittest.mock import Mock, patch, MagicMock
from PIL import Image

# Import the Flask app
from app import app
from core.barcode_scanner import BarcodeScanner
from core.listing import Listing


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application endpoints."""
    
    def setUp(self):
        """Set up test client and test data."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create test image
        self.test_image = Image.new('RGB', (100, 100), color='white')
        self.test_image_bytes = io.BytesIO()
        self.test_image.save(self.test_image_bytes, format='PNG')
        self.test_image_bytes.seek(0)
    
    def test_health_check_endpoint(self):
        """Test the health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        expected_data = {
            'status': 'healthy',
            'service': 'object-scanning-tool',
            'version': '1.0'
        }
        self.assertEqual(data, expected_data)
    
    def test_barcode_read_no_image(self):
        """Test barcode read endpoint without image."""
        response = self.client.post('/barcode/read')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'No image uploaded')
    
    @patch('app.BarcodeScanner.scan_image_for_barcode')
    def test_barcode_read_with_image(self, mock_scan):
        """Test barcode read endpoint with image."""
        mock_scan.return_value = 'test_barcode_123'
        
        response = self.client.post('/barcode/read', data={
            'image': (self.test_image_bytes, 'test.png')
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['barcode'], 'test_barcode_123')
    
    @patch('app.BarcodeScanner.scan_image_for_barcode')
    def test_barcode_read_no_barcode_found(self, mock_scan):
        """Test barcode read endpoint when no barcode is found."""
        mock_scan.return_value = None
        
        response = self.client.post('/barcode/read', data={
            'image': (self.test_image_bytes, 'test.png')
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['barcode'], None)
    
    def test_visual_match_endpoint(self):
        """Test visual match endpoint (not implemented yet)."""
        response = self.client.post('/visual/match')
        self.assertEqual(response.status_code, 501)
        
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'Visual match not implemented')
    
    def test_listing_from_images_no_images(self):
        """Test listing from images endpoint without images."""
        response = self.client.post('/listing/from-images')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'No images uploaded')
    
    @patch('app.Listing')
    @patch('app.BarcodeScanner')
    def test_listing_from_images_with_images(self, mock_scanner_class, mock_listing_class):
        """Test listing from images endpoint with images."""
        # Setup mocks
        mock_scanner = Mock()
        mock_scanner_class.return_value = mock_scanner
        
        mock_listing = Mock()
        mock_listing.to_dict.return_value = {'item': 'test_item', 'images': ['img1']}
        mock_listing_class.return_value = mock_listing
        
        # Prepare test data
        test_image_bytes_1 = io.BytesIO()
        self.test_image.save(test_image_bytes_1, format='PNG')
        test_image_bytes_1.seek(0)
        
        test_image_bytes_2 = io.BytesIO()
        self.test_image.save(test_image_bytes_2, format='PNG')
        test_image_bytes_2.seek(0)
        
        response = self.client.post('/listing/from-images', data={
            'images': [
                (test_image_bytes_1, 'test1.png'),
                (test_image_bytes_2, 'test2.png')
            ]
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {'item': 'test_item', 'images': ['img1']})
        
        # Verify mocks were called
        mock_scanner_class.assert_called_once()
        mock_listing_class.assert_called_once()
    
    def test_decision_image_missing_parameters(self):
        """Test decision image endpoint with missing parameters."""
        response = self.client.post('/decision/image', data={
            'image': (self.test_image_bytes, 'test.png')
            # Missing threshold parameter
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Image and threshold required')
    
    def test_decision_image_missing_image(self):
        """Test decision image endpoint with missing image."""
        response = self.client.post('/decision/image', data={
            'threshold': '0.5'
            # Missing image parameter
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Image and threshold required')
    
    def test_decision_image_not_implemented(self):
        """Test decision image endpoint (not fully implemented)."""
        response = self.client.post('/decision/image', data={
            'image': (self.test_image_bytes, 'test.png'),
            'threshold': '0.5'
        })
        
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.data)
        self.assertIn('Not implemented', data['result'])
    
    def test_decision_barcode_endpoint(self):
        """Test decision barcode endpoint (not implemented yet)."""
        test_data = {
            'barcode': 'test_barcode_123',
            'threshold': 0.5
        }
        
        response = self.client.post('/decision/barcode', 
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.data)
        self.assertIn('Not implemented', data['result'])
    
    def test_decision_barcode_no_json(self):
        """Test decision barcode endpoint without JSON data."""
        response = self.client.post('/decision/barcode')
        
        # Should handle gracefully even without JSON
        self.assertEqual(response.status_code, 501)


class TestAppMain(unittest.TestCase):
    """Test cases for the main function and CLI functionality."""
    
    @patch('app.PluginRegistry.available_types')
    @patch('sys.argv', ['app.py', 'test_type'])
    def test_main_with_valid_plugin_type(self, mock_available_types):
        """Test main function with valid plugin type."""
        mock_available_types.return_value = {
            'test_type': {'scanner': Mock(), 'builder': Mock()}
        }
        
        with patch('builtins.print') as mock_print:
            from app import main
            main()
            # Should print the plugin information
            mock_print.assert_called()
    
    @patch('app.PluginRegistry.available_types')
    @patch('sys.argv', ['app.py', 'invalid_type'])
    def test_main_with_invalid_plugin_type(self, mock_available_types):
        """Test main function with invalid plugin type."""
        mock_available_types.return_value = {}
        
        with patch('builtins.print') as mock_print:
            with patch('sys.exit') as mock_exit:
                from app import main
                main()
                # Should print error and exit
                mock_print.assert_called_with("No plugin registered for type 'invalid_type'")
                mock_exit.assert_called_with(1)
    
    @patch('sys.argv', ['app.py'])
    def test_main_with_no_arguments(self):
        """Test main function with no arguments."""
        with patch('builtins.print') as mock_print:
            with patch('sys.exit') as mock_exit:
                from app import main
                main()
                # Should print usage and exit
                mock_print.assert_called_with("Usage: python app.py <item_type> [args...]")
                mock_exit.assert_called_with(1)
    
    @patch('app.os.environ.get')
    @patch('sys.argv', ['flask'])
    def test_main_flask_mode(self, mock_env_get):
        """Test main function in Flask mode."""
        mock_env_get.side_effect = lambda key, default=None: {
            'FLASK_ENV': 'development'
        }.get(key, default)
        
        with patch('app.app.run') as mock_run:
            from app import main
            main()
            # Should run Flask app
            mock_run.assert_called_once_with(debug=True, host='0.0.0.0', port=5000)


class TestAppIntegration(unittest.TestCase):
    """Integration tests for the Flask application."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_app_routes_exist(self):
        """Test that all expected routes exist."""
        expected_routes = [
            '/health',
            '/barcode/read',
            '/visual/match',
            '/listing/from-images',
            '/decision/image',
            '/decision/barcode'
        ]
        
        # Get all routes from the app
        routes = [rule.rule for rule in self.app.url_map.iter_rules()]
        
        for expected_route in expected_routes:
            self.assertIn(expected_route, routes)
    
    def test_app_accepts_post_methods(self):
        """Test that POST methods are accepted on API endpoints."""
        api_endpoints = [
            '/barcode/read',
            '/visual/match',
            '/listing/from-images',
            '/decision/image',
            '/decision/barcode'
        ]
        
        for endpoint in api_endpoints:
            response = self.client.post(endpoint)
            # Should not return 405 Method Not Allowed
            self.assertNotEqual(response.status_code, 405)
    
    def test_health_check_always_available(self):
        """Test that health check is always available."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        # Should return valid JSON
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('service', data)
        self.assertIn('version', data)


if __name__ == '__main__':
    unittest.main() 