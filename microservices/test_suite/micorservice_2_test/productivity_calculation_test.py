import unittest
import subprocess
import requests

class TestYourFlaskApp(unittest.TestCase):

    def setUp(self):
        # Ensure that kubectl is installed and available in your shell
        # Replace 'your_pod_name' and 'your_service_name' with the actual values
        self.pod_name = 'productivity-cal-7748dd8568-4t9vh'
        self.service_name = 'productivity-cal'
        self.base_url = f'http://175.41.160.187:30007'

    def test_ping_endpoint(self):
        # Test the ping endpoint
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'SERVICE PING SUCCESSFUL : 200')

    def test_calculate_productivity_endpoint(self):
        # Test the calculate productivity endpoint
        response = requests.get(f'{self.base_url}/contributor/cal_produtivity')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected response

if __name__ == '__main__':
    unittest.main()
