
import unittest

from services.google_books_client import GoogleBooksClient
from models.book import Book


class TestGoogleBooksConversion(unittest.TestCase):

    def setUp(self):
        # Create a fresh GoogleBooksClient before each test.
        self.client = GoogleBooksClient()

        # Simulate the volumeInfo dictionary returned by Google Books.
        self.volume_info = {
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

    def test_convert_to_book(self):
        # ACT
        book = self.client._convert_to_book(self.volume_info)

        # ASSERT
        self.assertIsInstance(book, Book)
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
        volume_info = {
            "title": "Clean Code",
            "authors": ["Robert C. Martin"]
        }

        # ACT
        book = self.client._convert_to_book(volume_info)

        # ASSERT
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
        volume_info = {
            "title": "Clean Code",
            "authors": ["Robert C. Martin"]
        }

        # ACT
        book = self.client._convert_to_book(volume_info)

        # ASSERT
        self.assertIsNone(book.image_url)

    def test_convert_to_book_with_missing_title(self):
        # ARRANGE
        volume_info = {
            "authors": ["Robert C. Martin"]
        }

        # ACT & ASSERT
        with self.assertRaises(ValueError):
            self.client._convert_to_book(volume_info)

    def test_convert_to_book_with_missing_authors(self):
        # ARRANGE
        volume_info = {
            "title": "Clean Code"
        }

        # ACT
        book = self.client._convert_to_book(volume_info)

        # ASSERT
        self.assertEqual(book.title, "Clean Code")
        self.assertEqual(book.authors, [])


if __name__ == "__main__":
    unittest.main()
