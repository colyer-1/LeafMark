
import unittest
from models.book import Book


class TestBook(unittest.TestCase):

    def setUp(self):
        # Create a fresh Book instance before each test.
        self.book = Book(
            title="The Pragmatic Programmer",
            authors="David Thomas and Andrew Hunt",
            total_pages=352,
            published_date="2019-09"
        )

    def test_book_initialisation(self):
        # Check that the book information is stored correctly.
        self.assertEqual(self.book.title, "The Pragmatic Programmer")
        self.assertEqual(self.book.authors, "David Thomas and Andrew Hunt")
        self.assertEqual(self.book.total_pages, 352)
        self.assertEqual(self.book.published_date, "2019-09")

        # A new book should start with zero pages read.
        self.assertEqual(self.book.page_count, 0)
        self.assertFalse(self.book.is_finished)
        self.assertFalse(self.book.favourite)

    def test_optional_book_information(self):
        # Optional information should default to None.
        self.assertIsNone(self.book.subtitle)
        self.assertIsNone(self.book.description)
        self.assertIsNone(self.book.image_url)
        self.assertIsNone(self.book.average_rating)

    def test_book_can_be_created_with_only_required_information(self):
        # A book should be created without optional information.
        book = Book(
            title="Clean Code",
            authors="Robert C. Martin"
        )

        self.assertEqual(book.title, "Clean Code")
        self.assertEqual(book.authors, "Robert C. Martin")
        self.assertIsNone(book.total_pages)
        self.assertIsNone(book.published_date)

    def test_page_count_update(self):
        # Check that a valid page count can be assigned.
        self.book.page_count = 33

        self.assertEqual(self.book.page_count, 33)

    def test_page_count_rejects_invalid_values(self):
        # Page count must be an integer.
        with self.assertRaises(TypeError):
            self.book.page_count = "100"

        # Page count must not accept a boolean.
        with self.assertRaises(TypeError):
            self.book.page_count = True

        # Page count cannot be negative.
        with self.assertRaises(ValueError):
            self.book.page_count = -1

        # Page count cannot exceed the total number of pages.
        with self.assertRaises(ValueError):
            self.book.page_count = 353

    def test_progress_calculation(self):
        # Progress should be calculated as a percentage.
        self.book.page_count = 176
        self.assertEqual(self.book.progress, 50)

        self.book.page_count = 88
        self.assertEqual(self.book.progress, 25)

        self.book.page_count = 0
        self.assertEqual(self.book.progress, 0)

    def test_progress_when_total_pages_unknown(self):
        # Create a book without a known page count.
        book = Book(
            title="Clean Code",
            authors="Robert C. Martin"
        )

        # Progress cannot be calculated without total pages.
        self.assertIsNone(book.progress)

        # We should still be able to track pages read.
        book.page_count = 50
        self.assertEqual(book.page_count, 50)
        self.assertIsNone(book.progress)

    def test_reading_status(self):
        # A book with no pages read should not have started.
        self.assertEqual(self.book.reading_status, "Not started yet")

        # Reading some pages should change its status.
        self.book.page_count = 176
        self.assertEqual(self.book.reading_status, "In progress")

        # Reading all pages should mark the book as finished.
        self.book.page_count = 352
        self.assertEqual(self.book.reading_status, "Finished")

    def test_finished_status_updates_when_page_count_changes(self):
        # Reading the final page should mark the book as finished.
        self.book.page_count = 352
        self.assertTrue(self.book.is_finished)

        # Moving backwards should reset the finished status.
        self.book.page_count = 100
        self.assertFalse(self.book.is_finished)


if __name__ == "__main__":
    # Run the tests when this file is executed directly.
    unittest.main()
