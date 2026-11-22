
# Import os to check whether the test database file exists
# and remove it after each test.
import os

# Import sqlite3 so we can check for database errors.
import sqlite3

# Import unittest so we can create and run automated tests.
import unittest

# Import our Database class so we can test its functionality.
from services.database import Database

# Import our Book class
from models.book import Book


class TestDatabase(unittest.TestCase):
    """
    Contains tests for the Database class.
    """

    def setUp(self):
        """
        Runs before every test.

        Creates a separate database instance for testing.
        """

        # Use a separate database file for our tests.
        self.database_name = "test_leafmark.db"

        # Create a Database object using the test database filename.
        self.database = Database(self.database_name)

    def tearDown(self):
        """
        Runs after every test.

        Removes the test database file to prevent tests
        from interfering with one another.
        """

        # Check whether the test database file exists.
        if os.path.exists(self.database_name):

            # Remove the test database file.
            os.remove(self.database_name)

    def test_database_connection(self):
        """
        Tests that the Database class can establish a connection.
        """

        # ACT: Attempt to connect to the database.
        connection = self.database.connect()

        # ASSERT: Check that a connection was returned.
        self.assertIsNotNone(connection)

        # Close the database connection.
        connection.close()

    def test_database_file_is_created(self):
        """
        Tests that connecting to SQLite creates the database file
        if it does not already exist.
        """

        # ACT: Connect to the database.
        connection = self.database.connect()

        # ASSERT: Check that the database file exists.
        self.assertTrue(os.path.exists(self.database_name))

        # Close the database connection.
        connection.close()

    def test_create_books_table(self):
        """
        Tests that create_book_table() successfully creates
        the books table in the database.
        """

        # ACT: Create the books table.
        self.database.create_book_table()

        # Connect to the test database.
        connection = self.database.connect()

        try:
            # Create a cursor to execute SQL queries.
            cursor = connection.cursor()

            # Query SQLite's internal database information
            # to check whether a table called 'books' exists.
            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = 'books'
            """)

            # Retrieve the first matching result.
            # fetchone() returns None if no result is found.
            result = cursor.fetchone()

            # ASSERT: Check that the table exists.
            self.assertIsNotNone(result)

            # ASSERT: Check that the table has the correct name.
            self.assertEqual(result[0], "books")

        finally:
            # Always close the connection, even if the test fails.
            connection.close()

    def test_books_table_has_correct_columns(self):
        """
        Tests that the books table contains all expected columns
        in the correct order.
        """

        # ACT: Create the books table.
        self.database.create_book_table()

        # Connect to the test database.
        connection = self.database.connect()

        try:
            # Create a cursor to execute SQL queries.
            cursor = connection.cursor()

            # PRAGMA table_info retrieves information about
            # the columns belonging to the specified table.
            cursor.execute("PRAGMA table_info(books)")

            # Retrieve all column information returned by SQLite.
            columns = cursor.fetchall()

            # Each returned column contains several values.
            # Index 1 represents the column name.
            column_names = [column[1] for column in columns]

            # Define the columns we expect our books table to contain.
            expected_columns = [
                "id",
                "google_books_id",
                "title",
                "authors",
                "subtitle",
                "description",
                "total_pages",
                "page_count",
                "published_date",
                "image_url",
                "average_rating",
                "is_favourite"
            ]

            # ASSERT: Compare the actual column names
            # against the expected column names.
            self.assertEqual(column_names, expected_columns)

        finally:
            # Always close the connection.
            connection.close()

    def test_book_title_cannot_be_null(self):
        """
        Tests that SQLite prevents a book from being inserted
        without a title.
        """

        # ARRANGE: Create the books table.
        self.database.create_book_table()

        # Establish a connection to the test database.
        connection = self.database.connect()

        try:
            # Create a cursor to execute SQL queries.
            cursor = connection.cursor()

            # ACT and ASSERT:
            # Check that inserting NULL into the title column
            # raises an IntegrityError.
            with self.assertRaises(sqlite3.IntegrityError):

                cursor.execute("""
                    INSERT INTO books (title)
                    VALUES (NULL)
                """)

        finally:
            # Always close the database connection.
            connection.close()

        
    def test_google_books_id_must_be_unique(self):
        """
        Tests that SQLite prevents duplicate Google Books IDs.
        """

        # ARRANGE: Create the books table.
        self.database.create_book_table()

        # Connect to the test database.
        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            # Insert the first book.
            cursor.execute("""
                INSERT INTO books (google_books_id, title)
                VALUES (?, ?)
            """, ("google-book-123", "The Pragmatic Programmer"))

            # ACT and ASSERT:
            # Attempt to insert another book with the same Google Books ID.
            # SQLite should raise an IntegrityError.
            with self.assertRaises(sqlite3.IntegrityError):
                cursor.execute("""
                    INSERT INTO books (google_books_id, title)
                    VALUES (?, ?)
                """, ("google-book-123", "Another Book"))

        finally:
            connection.close()

        
    def test_book_default_values(self):
        """
        Tests that new books receive the correct default values.
        """

        # ARRANGE: Create the books table.
        self.database.create_book_table()

        # Connect to the test database.
        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            # ACT: Insert a book without specifying reading progress
            # or favourite status.
            cursor.execute("""
                INSERT INTO books (title)
                VALUES (?)
            """, ("The Pragmatic Programmer",))

            # Retrieve the values that SQLite stored.
            cursor.execute("""
                SELECT page_count, is_favourite
                FROM books
                WHERE title = ?
            """, ("The Pragmatic Programmer",))

            result = cursor.fetchone()

            # ASSERT: Check the default values.
            self.assertEqual(result[0], 0)
            self.assertEqual(result[1], 0)

        finally:
            connection.close()

    def test_add_book(self):
        # Create the database table.
        self.database.create_book_table()

        # Create a Book object to save.
        book = Book(
            id="google-book-123",
            title="The Pragmatic Programmer",
            authors=["Andrew Hunt", "David Thomas"],
            total_pages=352
        )

        # Add the book to the database.
        self.database.add_book(book)

        # Connect to the database to check the saved record.
        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT google_books_id, title, authors, total_pages
                FROM books
            """)

            result = cursor.fetchone()

            self.assertEqual(result[0], "google-book-123")
            self.assertEqual(result[1], "The Pragmatic Programmer")
            self.assertEqual(result[2], '["Andrew Hunt", "David Thomas"]')
            self.assertEqual(result[3], 352)

        finally:
            connection.close()

    def test_get_book(self):
        # Create the database table.
        self.database.create_book_table()

        # Create a Book object.
        book = Book(
            id="google-book-123",
            title="The Pragmatic Programmer",
            authors=["Andrew Hunt", "David Thomas"],
            total_pages=352
        )

        # Update the reading progress and favourite status.
        book.page_count = 100
        book.favourite = True

        # Save the book.
        self.database.add_book(book)

        # Retrieve the saved book.
        retrieved_book = self.database.get_book("google-book-123")

        # Check that a Book object was returned.
        self.assertIsInstance(retrieved_book, Book)

        # Check that the book information was restored.
        self.assertEqual(retrieved_book.id, "google-book-123")
        self.assertEqual(retrieved_book.title, "The Pragmatic Programmer")
        self.assertEqual(retrieved_book.authors, ["Andrew Hunt", "David Thomas"])
        self.assertEqual(retrieved_book.total_pages, 352)

        # Check that reading progress and favourite status were restored.
        self.assertEqual(retrieved_book.page_count, 100)
        self.assertTrue(retrieved_book.favourite)

    def test_get_book_returns_none_when_not_found(self):
        # Create the database table.
        self.database.create_book_table()

        # Try to retrieve a book that doesn't exist.
        result = self.database.get_book("non-existent-id")

        # Check that None is returned.
        self.assertIsNone(result)

    def test_remove_book(self):
        # Create the database table.
        self.database.create_book_table()

        # Create a Book object to save.
        book = Book(
            id="google-book-123",
            title="The Pragmatic Programmer",
            authors=["Andrew Hunt", "David Thomas"],
            total_pages=352
        )

        # Add the book to the database.
        self.database.add_book(book)

        # Remove the book using its Google Books ID.
        result = self.database.remove_book("google-book-123")

        # Check that the removal was successful.
        self.assertTrue(result)

        # Check that the book no longer exists in the database.
        retrieved_book = self.database.get_book("google-book-123")
        self.assertIsNone(retrieved_book)

    def test_remove_book_not_found(self):
        # Create the database table.
        self.database.create_book_table()

        # Try to remove a book that does not exist.
        result = self.database.remove_book("non-existent-id")

        # Check that the removal returns False.
        self.assertFalse(result)

    def test_get_all_books(self):
        # Create the database table.
        self.database.create_book_table()

        # Create two Book objects.
        first_book = Book(
            id="google-book-123",
            title="The Pragmatic Programmer",
            authors=["Andrew Hunt", "David Thomas"],
            total_pages=352
        )

        second_book = Book(
            id="google-book-456",
            title="Clean Code",
            authors=["Robert C. Martin"],
            total_pages=464
        )

        # Save both books to the database.
        self.database.add_book(first_book)
        self.database.add_book(second_book)

        # Retrieve all saved books.
        books = self.database.get_all_books()

        # Check that a list was returned.
        self.assertIsInstance(books, list)

        # Check that both books were retrieved.
        self.assertEqual(len(books), 2)

        # Check that the correct Book objects were returned.
        self.assertEqual(books[0].title, "The Pragmatic Programmer")
        self.assertEqual(books[1].title, "Clean Code")

        # Check that the retrieved objects are Book instances.
        self.assertIsInstance(books[0], Book)
        self.assertIsInstance(books[1], Book)

    def test_update_book(self):
        # Create the database table.
        self.database.create_book_table()

        # Create a Book object.
        book = Book(
            id="google-book-123",
            title="The Pragmatic Programmer",
            authors=["Andrew Hunt", "David Thomas"],
            total_pages=352
        )

        # Add the original book to the database.
        self.database.add_book(book)

        # Change the book's reading progress.
        book.page_count = 100

        # Mark the book as a favourite.
        book.favourite = True

        # Update the book in the database.
        result = self.database.update_book(book)

        # Check that the update was successful.
        self.assertTrue(result)

        # Retrieve the updated book.
        updated_book = self.database.get_book("google-book-123")

        # Check that the updated information was saved.
        self.assertEqual(updated_book.page_count, 100)
        self.assertTrue(updated_book.favourite)

    def test_update_book_not_found(self):
        # Create the database table.
        self.database.create_book_table()

        # Create a Book object that hasn't been saved.
        book = Book(
            id="non-existent-id",
            title="Unknown Book",
            authors=["Unknown Author"]
        )

        # Try to update the book.
        result = self.database.update_book(book)

        # Check that the update returns False.
        self.assertFalse(result)

    



# This condition ensures unittest.main() only runs when
# this file is executed directly, rather than imported by another module.
if __name__ == "__main__":
    unittest.main()
