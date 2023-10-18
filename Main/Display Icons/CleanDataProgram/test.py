import unittest
from ExtractLatLong import extract_lat_lng  # Import your function from your module

with open("google_api_key.txt", "r") as api_file:
    API_KEY = api_file.read().strip()

class TestGeocodeAPI(unittest.TestCase):

    def test_successful_geocoding(self):
        # Test a successful geocoding request
        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        data_type = "json"
        result = extract_lat_lng(API_KEY, address, data_type)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)

    def test_failed_request(self):
        # Test when the API request fails
        address = "Invalid Address"
        data_type = "json"
        result = extract_lat_lng(API_KEY, address, data_type)
        self.assertEqual(result, {})

    def test_missing_latlng(self):
        # Test when the API response is missing latitude and longitude
        address = "Some Location"
        data_type = "json"
        result = extract_lat_lng(API_KEY, address, data_type)
        self.assertEqual(result, (None, None))

if __name__ == '__main__':
    unittest.main()
