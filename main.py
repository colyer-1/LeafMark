
import requests
from dotenv import load_dotenv

from models.library import Library
from services.google_books_client import GoogleBooksClient
from ui.console import Console


# Load environment variables from the .env file.
load_dotenv()


# Create the objects needed by the application.
google_books = GoogleBooksClient()
library = Library()
ui = Console()


def run_book_menu(book):
    """Display and handle the selected book's menu."""

    while True:
        ui.clear_console()

        # Display the selected book's details.
        ui.display_book_details(book)

        # Display the available book actions.
        ui.display_menu(ui.book_menu)

        choice = ui.get_menu_choice(ui.book_menu)

        match choice:

            # Update the current reading page.
            case 1:
                ui.clear_console()

                ui.display_message(
                    f"Update reading progress: {book.title}"
                )

                page_number = ui.get_page_number(book.total_pages)

                if page_number is not None:
                    try:
                        book.page_count = page_number

                        ui.display_success_message(
                            "Reading progress updated."
                        )

                    except ValueError as error:
                        ui.display_error_message(str(error))

                ui.pause()

            # Remove the selected book from the library.
            case 2:
                try:
                    library.remove_book(book)

                    ui.display_success_message(
                        f"{book.title} removed from your library."
                    )

                except ValueError as error:
                    ui.display_error_message(str(error))

                ui.pause()
                return True

            # Display reading progress.
            case 3:
                ui.clear_console()
                ui.display_reading_progress(book)
                ui.pause()
            # Make book favourite/unfavourite
            case 4:
                if book.favourite:
                    book.favourite = False
                    ui.display_error_message(f"{book.title} has been removed from favourites")
                else:
                    book.favourite = True
                    ui.display_success_message(f"{book.title} has been added from favourites")
                ui.pause()
            # Return to the library menu.
            case 5:
                return True

            # Exit the application.
            case 0:
                return False


def run_library_menu():
    """Display and handle the library menu."""

    while True:
        ui.clear_console()
        ui.display_library_stats(library)
        ui.display_menu(ui.library_menu)

        choice = ui.get_menu_choice(ui.library_menu)

        match choice:

            # View all books in the library.
            case 1:
                ui.clear_console()
                ui.display_library_books(library)

                book_choice = ui.get_book_choice(library.books)

                if book_choice is not None:
                    app_running = run_book_menu(book_choice)

                    if not app_running:
                        return False

            # View favourite books.
            case 2:
                ui.clear_console()
                ui.display_favourites(library)
                ui.pause()

            # Return to the main menu.
            case 3:
                return True

            # Exit the application.
            case 0:
                return False


def search_google_books():
    """Search Google Books and allow the user to add a book."""

    ui.clear_console()

    # Ask the user for a search term.
    search_term = ui.get_search_term()

    try:
        # Retrieve books from the Google Books API.
        books = google_books.query_book(search_term, qty=9)

    except requests.exceptions.RequestException as error:
        ui.display_error_message(
            f"Unable to connect to Google Books: {error}"
        )
        ui.pause()
        return True

    # Display the search results.
    ui.clear_console()
    ui.display_search_results(books)

    # Allow the user to select a book.
    selected_book = ui.get_book_choice(books)

    if selected_book is None:
        return True

    # Display information about the selected book.
    ui.clear_console()
    ui.display_book_details(selected_book)

    # Display the Google Books menu.
    ui.display_menu(ui.google_book_menu)

    choice = ui.get_menu_choice(ui.google_book_menu)

    match choice:

        # Add the selected book to the library.
        case 1:
            try:
                library.add_book(selected_book)

                ui.display_success_message(
                    f"{selected_book.title} added to your library!"
                )

            except ValueError as error:
                ui.display_error_message(str(error))

            except TypeError as error:
                ui.display_error_message(str(error))

            ui.pause()
            return True

        # Return to the main menu.
        case 2:
            return True

        # Exit the application.
        case 0:
            return False


def main():
    """Start and manage the LeafMark application."""

    app_running = True

    ui.clear_console()
    ui.display_welcome_msg()
    ui.pause()

    while app_running:

        ui.clear_console()
        ui.display_menu(ui.main_menu)

        choice = ui.get_menu_choice(ui.main_menu)

        match choice:

            # Open the user's library.
            case 1:
                app_running = run_library_menu()

            # Search for books using Google Books.
            case 2:
                app_running = search_google_books()

            # Exit the application.
            case 0:
                app_running = False

    ui.clear_console()
    ui.display_message("Thank you for using LeafMark!")


# Only run the application when this file is executed directly.
if __name__ == "__main__":
    main()
