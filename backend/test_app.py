'''
Not meant to be comprehensive, just a simple demo for unit tests
'''


import unittest
from helpers import append_http


class TestAppendHttp(unittest.TestCase):
    def test_adds_http_to_plain_url(self):
        self.assertEqual(append_http("example.com"), "http://example.com")

    def test_keeps_existing_http(self):
        self.assertEqual(append_http("http://example.com"), "http://example.com")

    def test_keeps_existing_https(self):
        self.assertEqual(append_http("https://example.com"), "https://example.com")


if __name__ == "__main__":
    unittest.main()