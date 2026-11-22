
import unittest

from services.google_books_client import GoogleBooksClient
from models.book import Book


class TestGoogleBooksConversion(unittest.TestCase):

    def setUp(self):
        # Create a fresh GoogleBooksClient before each test.
        self.client = GoogleBooksClient()

        # Simulate a complete book item returned by Google Books.
        self.item = {
            "id": "google-book-123",
            "volumeInfo": {
                "title": "The Pragmatic Programmer",
                "subtitle": "Your Journey to Mastery",
                "authors": ["David Thomas", "Andrew Hunt"],
                "description": "A book about software development.",
                "pageCount": 352,
                "publishedDate": "2019-09",
                "imageLinks": {
                    "thumbnail": "https://example.com/book-cover.jpg"
                },
                "averageRating": 4.5
            }
        }

    def test_convert_to_book(self):
        # ACT
        book = self.client._convert_to_book(self.item)

        # ASSERT
        self.assertIsInstance(book, Book)
        self.assertEqual(book.id, "google-book-123")
        self.assertEqual(book.title, "The Pragmatic Programmer")
        self.assertEqual(book.subtitle, "Your Journey to Mastery")
        self.assertEqual(
            book.authors,
            ["David Thomas", "Andrew Hunt"]
        )
        self.assertEqual(
            book.description,
            "A book about software development."
        )
        self.assertEqual(book.total_pages, 352)
        self.assertEqual(book.published_date, "2019-09")
        self.assertEqual(
            book.image_url,
            "https://example.com/book-cover.jpg"
        )
        self.assertEqual(book.average_rating, 4.5)

    def test_convert_to_book_with_missing_optional_fields(self):
        # ARRANGE
        item = {
            "id": "google-book-456",
            "volumeInfo": {
                "title": "Clean Code",
                "authors": ["Robert C. Martin"]
            }
        }

        # ACT
        book = self.client._convert_to_book(item)

        # ASSERT
        self.assertEqual(book.id, "google-book-456")
        self.assertEqual(book.title, "Clean Code")
        self.assertEqual(book.authors, ["Robert C. Martin"])
        self.assertIsNone(book.subtitle)
        self.assertIsNone(book.description)
        self.assertIsNone(book.total_pages)
        self.assertIsNone(book.published_date)
        self.assertIsNone(book.image_url)
        self.assertIsNone(book.average_rating)

    def test_convert_to_book_with_missing_image_links(self):
        # ARRANGE
        item = {
            "id": "google-book-789",
            "volumeInfo": {
                "title": "Clean Code",
                "authors": ["Robert C. Martin"]
            }
        }

        # ACT
        book = self.client._convert_to_book(item)

        # ASSERT
        self.assertIsNone(book.image_url)

    def test_convert_to_book_with_missing_title(self):
        # ARRANGE
        item = {
            "id": "google-book-123",
            "volumeInfo": {
                "authors": ["Robert C. Martin"]
            }
        }

        # ACT & ASSERT
        with self.assertRaises(ValueError):
            self.client._convert_to_book(item)

    def test_convert_to_book_with_missing_authors(self):
        # ARRANGE
        item = {
            "id": "google-book-456",
            "volumeInfo": {
                "title": "Clean Code"
            }
        }

        # ACT
        book = self.client._convert_to_book(item)

        # ASSERT
        self.assertEqual(book.title, "Clean Code")
        self.assertEqual(book.authors, [])


if __name__ == "__main__":
    # Run the tests when this file is executed directly.
    unittest.main()
