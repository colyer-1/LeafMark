from models.book import Book
class Library:
    def __init__(self):
        self._books = []

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
        if book in self._books:
            raise ValueError("This book is already in your library")

        # Add the book to the collection.
        self._books.append(book)

    def remove_book(self, book):
        if not isinstance(book, Book):
            raise TypeError("Only Book objects can be added to the library")
                
        self._books.remove(book)

