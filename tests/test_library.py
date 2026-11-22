
import unittest

from models.book import Book
from models.library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Create a fresh library for each test.
        self.library = Library()

        # Create sample books for testing.
        self.book_one = Book(
            "The Pragmatic Programmer",
            "David Thomas and Andrew Hunt",
            352,
            "2019-09-13"
        )

        self.book_two = Book(
            "Clean Code",
            "Robert C. Martin",
            464,
            "2008-08-01"
        )

        self.book_three = Book(
            "Atomic Habits",
            "James Clear",
            320,
            "2018-10-16"
        )

        self.book_four = Book(
            "Deep Work",
            "Cal Newport",
            304,
            "2016-01-05"
        )

        self.book_five = Book(
            "The Hobbit",
            "J.R.R. Tolkien",
            310,
            "1937-09-21"
        )

        self.book_six = Book(
            "Think Like a Programmer",
            "V. Anton Spraul",
            256,
            "2012-08-12"
        )

    def test_add_book(self):
        # Add a book and check that it exists in the library.
        self.library.add_book(self.book_one)

        self.assertEqual(len(self.library._books), 1)
        self.assertIn(self.book_one, self.library._books)

    def test_add_multiple_books(self):
        # Add multiple books to the library.
        books = [
            self.book_one,
            self.book_two,
            self.book_three
        ]

        for book in books:
            self.library.add_book(book)

        self.assertEqual(len(self.library._books), 3)

    def test_add_invalid_object(self):
        # Only Book instances should be accepted.
        with self.assertRaises(TypeError):
            self.library.add_book("Not a book")

    def test_remove_book(self):
        # Add and then remove a book.
        self.library.add_book(self.book_one)
        self.library.remove_book(self.book_one)

        self.assertNotIn(self.book_one, self.library._books)

    def test_remove_invalid_object(self):
        # Only Book instances should be removable.
        with self.assertRaises(TypeError):
            self.library.remove_book("Not a book")

    def test_remove_book_not_in_library(self):
        # Removing a book that doesn't exist should raise ValueError.
        with self.assertRaises(ValueError):
            self.library.remove_book(self.book_one)


if __name__ == "__main__":
    # Run the tests when this file is executed directly.
    unittest.main()

        