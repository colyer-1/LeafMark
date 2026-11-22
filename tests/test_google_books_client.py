
import unittest

# Import patch to temporarily replace real functions during testing.
# Import Mock to create fake objects and simulate API responses.
from unittest.mock import patch, Mock

# Import requests so we can test HTTP exceptions.
import requests

# Import the class we want to tes 
from services.google_books_client import GoogleBooksClient


# Create a test class.
# unittest.TestCase provides the methods needed to write unit tests.
class TestGoogleBooksClient(unittest.TestCase):

    # setUp runs automatically before every individual test.
    # We create a fresh GoogleBooksClient for each test.
    def setUp(self):
        self.client = GoogleBooksClient()

    # Temporarily replace requests.get inside google_books_client
    # with a mock, so we don't make an actual HTTP request.
    @patch("services.google_books_client.requests.get")
    def test_query_book(self, mock_get):

        # ARRANGE
        # Prepare the conditions for our test.

        # Create a fake HTTP response.
        mock_response = Mock()

        # Configure the fake response so that calling .json()
        # returns our predefined dictionary.
        mock_response.json.return_value = {
            "totalItems": 1,
            "items": [
                {
                    "volumeInfo": {
                        "title": "The Pragmatic Programmer"
                    }
                }
            ]
        }

        # Configure the fake response to represent a successful HTTP request.
        mock_response.raise_for_status.return_value = None

        # Tell the mocked requests.get() to return our fake response.
        mock_get.return_value = mock_response

        # ACT
        # Execute the method we're testing.
        result = self.client.query_book("The Pragmatic Programmer")

        # ASSERT
        # Check whether the returned book title matches our expectation.
        self.assertEqual(
            result[0].title,
            "The Pragmatic Programmer"
        )

        # Check that requests.get() was called exactly once
        # with the expected URL and search parameters.
        mock_get.assert_called_once_with(
            GoogleBooksClient.BASE_URL,
            params={
                "q": "The Pragmatic Programmer",
                "key": self.client.api_key,
                "maxResults": 10,
            }
        )

    # Test how the client behaves when the HTTP request fails.
    @patch("services.google_books_client.requests.get")
    def test_query_book_raises_http_error(self, mock_get):

        # ARRANGE
        # Create a fake HTTP response.
        mock_response = Mock()

        # Configure raise_for_status() to raise an HTTPError.
        # This simulates an HTTP error, such as a 429 Too Many Requests.
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "429 Client Error: Too Many Requests"
        )

        # Tell the mocked requests.get() to return our fake response.
        mock_get.return_value = mock_response

        # ACT & ASSERT
        # Check that calling query_book() raises an HTTPError.
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.query_book("Harry Potter")
