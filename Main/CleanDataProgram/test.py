import unittest
from ExtractLatLong import extract_lat_lng  # Import your function from your module

with open("google_api_key.txt", "r") as api_file:
    API_KEY = api_file.read().strip()

class TestGeocodeAPI(unittest.TestCase):
    
    def test_valid_address(self):
    # Test with a valid address
        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        result = extract_lat_lng(address)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        
    def test_invalid_address(self):
        # Test with an invalid address (e.g., "ThisIsNotAnAddress")
        address = "john"
        result = extract_lat_lng(address)
        expected = (None, None)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
