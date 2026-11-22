
# Import os to identify the operating system.
import os

# Import subprocess to execute terminal commands.
import subprocess


class Console:
    """
    Handles all terminal input and output for LeafMark.

    Responsible for displaying menus, book information,
    library information and collecting user input.
    """

    # Terminal text colours.
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    def __init__(self):

        # Main application menu.
        self._main_menu = {
            "title": "Main Menu",
            "options": ["Library", "Book search"]
        }

        # Individual book menu.
        self._book_menu = {
            "title": "Book Options",
            "options": [
                "Read",
                "Remove from Library",
                "Progress",
                "Favourite/Unfavorite",
                "Main menu"
            ]
        }

        # Google Books search result menu.
        self._google_book_menu = {
            "title": "Google Book",
            "options": ["Add to library", "Main menu"]
        }

        # Personal library menu.
        self._library_menu = {
            "title": "Library",
            "options": ["Books", "Favourites", "Main menu"]
        }

    # --------------------------------------------------
    # MENU PROPERTIES
    # --------------------------------------------------

    @property
    def main_menu(self):
        return self._main_menu

    @property
    def book_menu(self):
        return self._book_menu

    @property
    def google_book_menu(self):
        return self._google_book_menu

    @property
    def library_menu(self):
        return self._library_menu

    # --------------------------------------------------
    # TERMINAL DISPLAY
    # --------------------------------------------------

    def clear_console(self):
        """Clear the terminal screen."""

        command = "cls" if os.name == "nt" else "clear"

        subprocess.run(command, shell=True, check=False)

    def display_welcome_msg(self):
        """Display the application's welcome message."""

        print("\n" + "=" * 30)
        print("          LeafMark")
        print("       Personal library")
        print("=" * 30)

    def display_menu(self, menu):
        """Display a menu using the options supplied."""

        print(f"\n{'=' * 30}")
        print(menu["title"])
        print("=" * 30)

        for i, option in enumerate(menu["options"], start=1):
            print(f"{i}. {option}")

        print("0. Exit")

    def pause(self, message="Press Enter to continue..."):
        """Pause execution until the user presses Enter."""

        input(f"\n{message}")

    # --------------------------------------------------
    # USER INPUT
    # --------------------------------------------------

    def get_menu_choice(self, menu):
        """Collect a valid menu selection."""

        while True:
            try:
                user_choice = int(input("> "))

                # Allow 0 as an exit option.
                if user_choice == 0:
                    return user_choice

                # Check whether the selection exists.
                if 1 <= user_choice <= len(menu["options"]):
                    return user_choice

                print(
                    f"Please choose a number between "
                    f"1 and {len(menu['options'])}, or 0 to exit."
                )

            except ValueError:
                print("Please enter a valid number.")

    def get_search_term(self):
        """Collect a non-empty book search term."""

        while True:
            search_term = input("\nSearch for a book: ").strip()

            if search_term:
                return search_term

            self.display_error_message(
                "Search term cannot be empty."
            )

    def get_book_choice(self, books):
        """
        Collect a book selection.

        Returns the selected Book object or None if the user
        chooses to go back.
        """

        if not books:
            self.pause()
            return None

        while True:
            try:
                user_choice = int(input("\nSelect a book: "))

                # Return None when the user chooses to go back.
                if user_choice == 0:
                    return None

                # Check whether the selection matches a book.
                if 1 <= user_choice <= len(books):
                    return books[user_choice - 1]

                print(
                    f"Please choose a number between "
                    f"1 and {len(books)}, or 0 to go back."
                )

            except ValueError:
                print("Please enter a valid number.")

    def get_page_number(self, total_pages):
        """Collect and validate the user's current reading page."""

        while True:
            try:
                page_number = int(
                    input("\nEnter your current page (0 to cancel): ")
                )

                if page_number == 0:
                    return None

                if page_number < 0:
                    print("Page number cannot be negative.")
                    continue

                if total_pages and page_number > total_pages:
                    print(
                        f"This book only has {total_pages} pages."
                    )
                    continue

                return page_number

            except ValueError:
                print("Please enter a valid page number.")

    # --------------------------------------------------
    # GOOGLE BOOKS DISPLAY
    # --------------------------------------------------

    def display_search_results(self, books):
        """Display books returned by the Google Books API."""

        if not books:
            self.display_error_message("No books found.")
            return

        print("\nSearch Results")
        print("=" * 30)

        for i, book in enumerate(books, start=1):

            authors = (
                ", ".join(book.authors)
                if book.authors
                else "Unknown author"
            )

            print(f"{i}. {book.title} - {authors}")

        print("\n0. Back")

    def display_book_details(self, book):
        """Display detailed information about an individual book."""

        print("\n" + "=" * 40)
        print("BOOK DETAILS")
        print("=" * 40)

        self.display_book(book)

        print("=" * 40)

    def display_book(self, book):
        """Display the information available for a Book object."""

        print(f"Title: {book.title}")

        authors = (
            ", ".join(book.authors)
            if book.authors
            else "Unknown author"
        )

        print(f"Authors: {authors}")

        if book.subtitle:
            print(f"Subtitle: {book.subtitle}")

        if book.published_date:
            print(f"Published: {book.published_date}")

        print(f"Current page: {book.page_count}")

        if book.total_pages:
            print(f"Pages: {book.total_pages}")

        if book.favourite:
            print("Favourite: Yes")
        else:
            print("Favourite: No")

        if book.average_rating is not None:
            print(f"Rating: {book.average_rating}/5")

        if book.description:
            print(f"\nDescription:\n{book.description}")

    # --------------------------------------------------
    # LIBRARY DISPLAY
    # --------------------------------------------------

    def display_library_stats(self, library):
        """Display statistics about the user's library."""

        total_books = library.total_books

        print("\n" + "=" * 30)
        print("LIBRARY STATISTICS")
        print("=" * 30)

        if total_books < 1:
            self.display_message(
                "You have no books in your library."
            )
        else:
            print(f"Total books: {total_books}")

    def display_library_books(self, library):
        """Display all books currently stored in the library."""

        books = library.books

        if not books:
            self.display_error_message(
                "Your library is empty."
            )
            return

        print("\nYour Library")
        print("=" * 30)

        for i, book in enumerate(books, start=1):

            authors = (
                ", ".join(book.authors)
                if book.authors
                else "Unknown author"
            )

            print(f"{i}. {book.title} - {authors}")

    def display_favourites(self, library):
        """Display the user's favourite books."""

        favourites = [
            book for book in library.books
            if book.favourite
        ]

        if not favourites:
            self.display_message(
                "You haven't added any favourite books yet."
            )
            return

        print("\nYour Favourite Books")
        print("=" * 30)

        for i, book in enumerate(favourites, start=1):
            print(f"{i}. {book.title}")

    def display_reading_progress(self, book):
        """Display the reading progress of an individual book."""

        if not book.total_pages:
            self.display_message(
                "Page count information is unavailable for this book."
            )
            return

        progress = (
            book.page_count / book.total_pages
        ) * 100

        print("\n" + "=" * 30)
        print("READING PROGRESS")
        print("=" * 30)

        print(f"Book: {book.title}")
        print(f"Current page: {book.page_count}")
        print(f"Total pages: {book.total_pages}")
        print(f"Progress: {progress:.1f}%")

    # --------------------------------------------------
    # MESSAGES
    # --------------------------------------------------

    def display_message(self, message):
        """Display a general application message."""

        print(f"\n{message}")

    def display_success_message(self, message):
        """Display a green success message."""

        print(f"\n{self.GREEN}{message}{self.RESET}")

    def display_error_message(self, message):
        """Display a red error message."""

        print(f"\n{self.RED}{message}{self.RESET}")

    def display_warning_message(self, message):
        """Display a yellow warning message."""

        print(f"\n{self.YELLOW}{message}{self.RESET}")
