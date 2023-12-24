import unittest
import requests

class TestFetchGitData(unittest.TestCase):
    def setUp(self):
        # Set the base URL for your service
        self.base_url = "http://175.41.160.187:30006"

    def test_get_contributions_endpoint(self):
        # Make a request to the /contributor/get_contributions endpoint
        response = requests.get(f"{self.base_url}/contributor/get_contributions")

        # Assertions
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        
        # Assuming the response should be in JSON format
        json_response = response.json()
        self.assertIsInstance(json_response, list, "Expected a list in the response")

        # Add more assertions based on the actual response structure

if __name__ == '__main__':
    unittest.main()
