'''
Not meant to be comprehensive, just a simple demo for unit tests
'''


import unittest
import psycopg2.pool
from unittest.mock import patch


class TestApi(unittest.TestCase):
    def test_shorten_no_body(self):
        # prevent connecting to database
        with patch("psycopg2.pool.SimpleConnectionPool", return_value=None):
            from app import app

            client = app.test_client()
            
            response = client.post("/api/v1/shorten", json={})
            
            self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
