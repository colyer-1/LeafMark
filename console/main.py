import requests
from dotenv import load_dotenv

from models.library import Library
from services.database import Database
from services.google_books_client import GoogleBooksClient
from ui.console import Console


def run_book_menu(book, library, ui):
    """Display and handle the selected book's menu."""

    while True:
        ui.clear_console()
        ui.display_book_details(book)
        ui.display_menu(ui.book_menu)

        choice = ui.get_menu_choice(ui.book_menu)

        match choice:

            # Update the current reading page.
            case 1:
                ui.clear_console()
                ui.display_message(
                    f"Update reading progress: {book.title}"
                )

                # Ask the user for their current reading page.
                page_number = ui.get_page_number(book.total_pages)

                if page_number is not None:
                    try:
                        # Update the Book object's reading progress.
                        book.page_count = page_number

                        # Save the updated book to the database.
                        library.update_book(book)

                        ui.display_success_message(
                            "Reading progress updated."
                        )

                    except (ValueError, TypeError) as error:
                        ui.display_error_message(str(error))

                    except requests.exceptions.RequestException as error:
                        ui.display_error_message(
                            f"Unable to update reading progress: {error}"
                        )

                    except Exception as error:
                        ui.display_error_message(
                            f"Unable to save reading progress: {error}"
                        )

                ui.pause()

            # Remove the selected book from the library.
            case 2:
                try:
                    # Remove the book from the library and database.
                    library.remove_book(book)

                    ui.display_success_message(
                        f"{book.title} removed from your library."
                    )

                except (ValueError, TypeError) as error:
                    ui.display_error_message(str(error))

                except Exception as error:
                    ui.display_error_message(
                        f"Unable to remove book: {error}"
                    )

                ui.pause()
                return True

            # Display reading progress.
            case 3:
                ui.clear_console()
                ui.display_reading_progress(book)
                ui.pause()

            # Toggle favourite status.
            case 4:
                try:
                    # Reverse the current favourite status.
                    book.favourite = not book.favourite

                    # Save the updated favourite status.
                    library.update_book(book)

                    if book.favourite:
                        ui.display_success_message(
                            f"{book.title} added to favourites."
                        )
                    else:
                        ui.display_message(
                            f"{book.title} removed from favourites."
                        )

                except Exception as error:
                    ui.display_error_message(
                        f"Unable to update favourite status: {error}"
                    )

                ui.pause()

            # Return to the library menu.
            case 5:
                return True

            # Exit the application.
            case 0:
                return False


def run_library_menu(library, ui):
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

                # Allow the user to select a book.
                selected_book = ui.get_book_choice(library.books)

                if selected_book is not None:
                    app_running = run_book_menu(
                        selected_book,
                        library,
                        ui
                    )

                    if not app_running:
                        return False

            # View favourite books.
            case 2:
                ui.clear_console()
                ui.display_favourites(library)
                selected_book = ui.get_book_choice(library.books)
                if selected_book is not None:
                    app_running = run_book_menu(
                        selected_book,
                        library,
                        ui
                    )
                
                    if not app_running:
                        return False
                ui.pause()

            # Return to the main menu.
            case 3:
                return True

            # Exit the application.
            case 0:
                return False


def search_google_books(google_books, library, ui):
    """Search Google Books and allow the user to add a book."""

    ui.clear_console()

    # Ask the user what book they want to search for.
    search_term = ui.get_search_term()

    try:
        # Request matching books from the Google Books API.
        books = google_books.query_book(search_term, qty=9)

    except requests.exceptions.RequestException as error:
        ui.display_error_message(
            f"Unable to connect to Google Books: {error}"
        )
        ui.pause()
        return True

    ui.clear_console()

    # Display the books returned by the Google Books API.
    ui.display_search_results(books)

    # Allow the user to select a search result.
    selected_book = ui.get_book_choice(books)

    if selected_book is None:
        return True

    ui.clear_console()
    ui.display_book_details(selected_book)
    ui.display_menu(ui.google_book_menu)

    choice = ui.get_menu_choice(ui.google_book_menu)

    match choice:

        # Add the selected book to the library.
        case 1:
            try:
                # Add the book to the library and save it to SQLite.
                library.add_book(selected_book)

                ui.display_success_message(
                    f"{selected_book.title} added to your library!"
                )

            except (ValueError, TypeError) as error:
                ui.display_error_message(str(error))

            except Exception as error:
                ui.display_error_message(
                    f"Unable to add book: {error}"
                )

            ui.pause()
            return True

        # Return to the main menu.
        case 2:
            return True

        # Exit the application.
        case 0:
            return False


def main():
    """Create application dependencies and run LeafMark."""

    # Load environment variables from the .env file.
    load_dotenv()

    # Create the SQLite database connection manager.
    database = Database()

    # Create the database tables if they do not already exist.
    database.create_book_table()

    # Create the Google Books API client.
    google_books = GoogleBooksClient()

    # Create the library and load previously saved books.
    library = Library(database)

    # Create the console interface.
    ui = Console()

    # Track whether the application should continue running.
    app_running = True

    # Display the welcome message when the application starts.
    ui.clear_console()
    ui.display_welcome_msg()
    ui.pause()

    # Main application loop.
    while app_running:
        ui.clear_console()
        ui.display_menu(ui.main_menu)

        choice = ui.get_menu_choice(ui.main_menu)

        match choice:

            # Open the user's library.
            case 1:
                app_running = run_library_menu(library, ui)

            # Search Google Books.
            case 2:
                app_running = search_google_books(
                    google_books,
                    library,
                    ui
                )

            # Exit the application.
            case 0:
                app_running = False

    # Display the exit message.
    ui.clear_console()
    ui.display_message("Thank you for using LeafMark!")


# Only run the application when this file is executed directly.
if __name__ == "__main__":
    main()
