import os
import tempfile
import unittest

from models.book import Book
from models.library import Library
from services.database import Database


class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the test database.
        self.temp_directory = tempfile.TemporaryDirectory()

        # Register cleanup to run after each test.
        self.addCleanup(self.temp_directory.cleanup)

        # Create a path for the test database.
        database_path = os.path.join(
            self.temp_directory.name,
            "test_leafmark.db"
        )

        # Create the database object.
        self.database = Database(database_path)

        # Create the database tables.
        self.database.create_book_table()

        # Create a fresh library using the test database.
        self.library = Library(self.database)

        # Create sample books for testing.
        self.book_one = Book(
            "google-book-1",
            "The Pragmatic Programmer",
            ["David Thomas", "Andrew Hunt"],
            352,
            published_date="2019-09-13"
        )

        self.book_two = Book(
            "google-book-2",
            "Clean Code",
            ["Robert C. Martin"],
            464,
            published_date="2008-08-01"
        )

        self.book_three = Book(
            "google-book-3",
            "Atomic Habits",
            ["James Clear"],
            320,
            published_date="2018-10-16"
        )

        self.book_four = Book(
            "google-book-4",
            "Deep Work",
            ["Cal Newport"],
            304,
            published_date="2016-01-05"
        )

        self.book_five = Book(
            "google-book-5",
            "The Hobbit",
            ["J.R.R. Tolkien"],
            310,
            published_date="1937-09-21"
        )

        self.book_six = Book(
            "google-book-6",
            "Think Like a Programmer",
            ["V. Anton Spraul"],
            256,
            published_date="2012-08-12"
        )

    def test_add_book(self):
        # Add a book and check that it exists in the library.
        self.library.add_book(self.book_one)

        self.assertEqual(self.library.total_books, 1)
        self.assertIn(self.book_one, self.library.books)

        # Check that the book was also saved to the database.
        saved_book = self.database.get_book(self.book_one.id)

        self.assertIsNotNone(saved_book)
        self.assertEqual(saved_book.title, self.book_one.title)

    def test_add_multiple_books(self):
        # Add multiple books to the library.
        books = [
            self.book_one,
            self.book_two,
            self.book_three
        ]

        for book in books:
            self.library.add_book(book)

        self.assertEqual(self.library.total_books, 3)

    def test_add_invalid_object(self):
        # Only Book instances should be accepted.
        with self.assertRaises(TypeError):
            self.library.add_book("Not a book")

    def test_remove_book(self):
        # Add and then remove a book.
        self.library.add_book(self.book_one)
        self.library.remove_book(self.book_one)

        self.assertNotIn(self.book_one, self.library.books)

        # Check that the book was also removed from the database.
        self.assertIsNone(
            self.database.get_book(self.book_one.id)
        )

    def test_remove_invalid_object(self):
        # Only Book instances should be removable.
        with self.assertRaises(TypeError):
            self.library.remove_book("Not a book")

    def test_remove_book_not_in_library(self):
        # Removing a book that doesn't exist should raise ValueError.
        with self.assertRaises(ValueError):
            self.library.remove_book(self.book_one)

    
    def test_books_persist_after_creating_new_library(self):
        # Add a book to the first library.
        self.library.add_book(self.book_one)

        # Create a new library using the same database.
        new_library = Library(self.database)

        # Check that the book was loaded into the new library.
        self.assertEqual(new_library.total_books, 1)

        # Check that the saved book has the correct information.
        saved_book = new_library.books[0]

        self.assertEqual(saved_book.id, self.book_one.id)
        self.assertEqual(saved_book.title, self.book_one.title)
        self.assertEqual(saved_book.authors, self.book_one.authors)

    def test_update_book(self):
        # Add a book to the library.
        self.library.add_book(self.book_one)

        # Change the book's reading progress and favourite status.
        self.book_one.page_count = 50
        self.book_one.favourite = True

        # Update the book in the database.
        self.library.update_book(self.book_one)

        # Retrieve the updated book from the database.
        updated_book = self.database.get_book(self.book_one.id)

        # Check that the changes were saved.
        self.assertEqual(updated_book.page_count, 50)
        self.assertTrue(updated_book.favourite)

    def test_update_invalid_object(self):
        # Only Book instances should be updated.
        with self.assertRaises(TypeError):
            self.library.update_book("Not a book")

    def test_update_book_not_in_library(self):
        # Updating a book that doesn't exist should raise ValueError.
        with self.assertRaises(ValueError):
            self.library.update_book(self.book_one)


if __name__ == "__main__":
    # Run the tests when this file is executed directly.
    unittest.main()