
from models.book import Book


class Library:
    """
    Manages the user's collection of books.
    """

    def __init__(self, database):
        # Store the database object.
        self._database = database

        # Load previously saved books from the database.
        self._books = self._database.get_all_books()

    @property
    def books(self):
        return self._books

    @property
    def total_books(self):
        return len(self._books)

    @property
    def favourite_books(self):
        favourite_books = []

        for book in self._books:
            if book.favourite:
                favourite_books.append(book)

        return favourite_books

    def add_book(self, book):
        # Check that the supplied object is a Book.
        if not isinstance(book, Book):
            raise TypeError("Only Book objects can be added to the library")

        # Prevent the same book object from being added twice.
        # Prevent books with the same Google Books ID from being added twice.
        for existing_book in self._books:
            if existing_book.id == book.id:
                raise ValueError("This book is already in your library")

        # Save the book to the database.
        self._database.add_book(book)

        # Add the book to the collection.
        self._books.append(book)

    def remove_book(self, book):
        # Check that the supplied object is a Book.
        if not isinstance(book, Book):
            raise TypeError("Only Book objects can be removed from the library")

        # Check that the book exists in the library.
        if book not in self._books:
            raise ValueError("This book is not in your library")

        # Remove the book from the database.
        self._database.remove_book(book.id)

        # Remove the book from the collection.
        self._books.remove(book)

    def update_book(self, book):
        """
        Update an existing book in the library and database.
        """

        # Check that the supplied object is a Book.
        if not isinstance(book, Book):
            raise TypeError("Only Book objects can be updated")

        # Check that the book exists in the library.
        if book not in self._books:
            raise ValueError("This book is not in your library")

        # Update the book in the database.
        self._database.update_book(book)
