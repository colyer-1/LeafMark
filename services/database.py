
import sqlite3
import json

from models.book import Book


class Database:
    """
    Handles the SQLite database connection and database
    operations for the LeafMark application.
    """

    def __init__(self, database_name="leafmark.db"):
        # Store the name of the database file.
        self.database_name = database_name

    def connect(self):
        """
        Establish and return a connection to the database.
        """

        # Connect to the SQLite database.
        # SQLite automatically creates the file if it does not exist.
        connection = sqlite3.connect(self.database_name)

        return connection

    def create_book_table(self):
        """
        Create the books table if it does not already exist.
        """

        # Establish a connection to the database.
        connection = self.connect()

        try:
            # Create a cursor to execute SQL statements.
            cursor = connection.cursor()

            # Create the books table and define its columns.
            # IF NOT EXISTS prevents an error if the table already exists.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    google_books_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    authors TEXT,
                    subtitle TEXT,
                    description TEXT,
                    total_pages INTEGER,
                    page_count INTEGER NOT NULL DEFAULT 0,
                    published_date TEXT,
                    image_url TEXT,
                    average_rating REAL,
                    is_favourite INTEGER NOT NULL DEFAULT 0
                )
            """)

            # Save the changes to the database.
            connection.commit()

        finally:
            # Always close the database connection.
            connection.close()

    def add_book(self, book):
        """
        Add a Book object to the database.
        """

        # Establish a connection to the database.
        connection = self.connect()

        try:
            # Create a cursor to execute SQL statements.
            cursor = connection.cursor()

            # Insert the book information into the books table.
            # Question marks act as placeholders for the supplied values.
            cursor.execute("""
                INSERT INTO books (
                    google_books_id,
                    title,
                    authors,
                    subtitle,
                    description,
                    total_pages,
                    page_count,
                    published_date,
                    image_url,
                    average_rating,
                    is_favourite
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book.id,
                book.title,
                json.dumps(book.authors),
                book.subtitle,
                book.description,
                book.total_pages,
                book.page_count,
                book.published_date,
                book.image_url,
                book.average_rating,
                int(book.favourite)
            ))

            # Save the inserted book to the database.
            connection.commit()

        finally:
            # Always close the database connection.
            connection.close()

    def get_book(self, google_books_id):
        """
        Retrieve a book from the database using its Google Books ID.
        """

        # Establish a connection to the database.
        connection = self.connect()

        try:
            # Create a cursor to execute SQL statements.
            cursor = connection.cursor()

            # Search for a book matching the supplied Google Books ID.
            cursor.execute("""
                SELECT
                    google_books_id,
                    title,
                    authors,
                    subtitle,
                    description,
                    total_pages,
                    page_count,
                    published_date,
                    image_url,
                    average_rating,
                    is_favourite
                FROM books
                WHERE google_books_id = ?
            """, (google_books_id,))

            # Retrieve the matching database record.
            result = cursor.fetchone()

            # Return None if the book does not exist.
            if result is None:
                return None

            # Reconstruct a Book object using the database information.
            book = Book(
                id=result[0],
                title=result[1],
                authors=json.loads(result[2]) if result[2] else [],
                total_pages=result[5],
                subtitle=result[3],
                description=result[4],
                published_date=result[7],
                image_url=result[8],
                average_rating=result[9]
            )

            # Restore the book's saved reading progress.
            book.page_count = result[6]

            # Convert the stored integer back into a boolean.
            book.favourite = bool(result[10])

            return book

        finally:
            # Always close the database connection.
            connection.close()

    def get_all_books(self):
        """
        Retrieve all books from the database.
        """

        # Establish a connection to the database.
        connection = self.connect()

        try:
            # Create a cursor to execute SQL statements.
            cursor = connection.cursor()

            # Retrieve all books from the books table.
            cursor.execute("""
                SELECT
                    google_books_id,
                    title,
                    authors,
                    subtitle,
                    description,
                    total_pages,
                    page_count,
                    published_date,
                    image_url,
                    average_rating,
                    is_favourite
                FROM books
            """)

            # Retrieve all matching database records.
            results = cursor.fetchall()

            # Create an empty list to store the Book objects.
            books = []

            # Loop through each database record.
            for result in results:

                # Reconstruct a Book object from the database record.
                book = Book(
                    id=result[0],
                    title=result[1],
                    authors=json.loads(result[2]) if result[2] else [],
                    total_pages=result[5],
                    subtitle=result[3],
                    description=result[4],
                    published_date=result[7],
                    image_url=result[8],
                    average_rating=result[9]
                )

                # Restore the saved reading progress.
                book.page_count = result[6]

                # Restore the saved favourite status.
                book.favourite = bool(result[10])

                # Add the reconstructed Book object to the list.
                books.append(book)

            # Return all retrieved books.
            return books

        finally:
            # Always close the database connection.
            connection.close()

    def remove_book(self, google_books_id):
        """
        Remove a book from the database using its Google Books ID.
        """

        # Establish a connection to the database.
        connection = self.connect()

        try:
            # Create a cursor to execute SQL statements.
            cursor = connection.cursor()

            # Delete the book matching the supplied Google Books ID.
            cursor.execute("""
                DELETE FROM books
                WHERE google_books_id = ?
            """, (google_books_id,))

            # Save the deletion to the database.
            connection.commit()

            # rowcount tells us how many database records were affected.
            # Return True if a book was deleted, otherwise return False.
            return cursor.rowcount > 0

        finally:
            # Always close the database connection.
            connection.close()

    def update_book(self, book):
        """
        Update an existing book in the database.
        """

        # Establish a connection to the database.
        connection = self.connect()

        try:
            # Create a cursor to execute SQL statements.
            cursor = connection.cursor()

            # Update the book information using its Google Books ID.
            cursor.execute("""
                UPDATE books
                SET
                    title = ?,
                    authors = ?,
                    subtitle = ?,
                    description = ?,
                    total_pages = ?,
                    page_count = ?,
                    published_date = ?,
                    image_url = ?,
                    average_rating = ?,
                    is_favourite = ?
                WHERE google_books_id = ?
            """, (
                book.title,
                json.dumps(book.authors),
                book.subtitle,
                book.description,
                book.total_pages,
                book.page_count,
                book.published_date,
                book.image_url,
                book.average_rating,
                int(book.favourite),
                book.id
            ))

            # Save the changes to the database.
            connection.commit()

            # Return True if a record was updated.
            return cursor.rowcount > 0

        finally:
            # Always close the database connection.
            connection.close()

