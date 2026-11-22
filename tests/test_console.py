
import unittest

from io import StringIO
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from ui.console import Console


class TestConsole(unittest.TestCase):

    def setUp(self):
        """Create a fresh Console and sample books before each test."""

        self.ui = Console()

        self.book_one = SimpleNamespace(
            title="The Hobbit",
            authors=["J.R.R. Tolkien"],
            subtitle=None,
            published_date="1937",
            page_count=100,
            total_pages=300,
            favourite=True,
            average_rating=4.5,
            description="A hobbit goes on an adventure."
        )

        self.book_two = SimpleNamespace(
            title="Dune",
            authors=["Frank Herbert"],
            subtitle=None,
            published_date="1965",
            page_count=0,
            total_pages=500,
            favourite=False,
            average_rating=4.2,
            description="A science fiction novel."
        )

        self.books = [self.book_one, self.book_two]

        self.library = SimpleNamespace(
            books=self.books,
            total_books=len(self.books)
        )

    # --------------------------------------------------
    # MENU PROPERTY TESTS
    # --------------------------------------------------

    def test_main_menu(self):
        """Test that the main menu contains the correct options."""

        self.assertEqual(
            self.ui.main_menu["options"],
            ["Library", "Book search"]
        )

    def test_book_menu(self):
        """Test that the book menu contains the correct options."""

        self.assertEqual(
            self.ui.book_menu["options"],
            [
                "Read",
                "Remove from Library",
                "Progress",
                "Favourite/Unfavorite",
                "Main menu"
            ]
        )

    def test_google_book_menu(self):
        """Test that the Google Books menu contains the correct options."""

        self.assertEqual(
            self.ui.google_book_menu["options"],
            ["Add to library", "Main menu"]
        )

    def test_library_menu(self):
        """Test that the library menu contains the correct options."""

        self.assertEqual(
            self.ui.library_menu["options"],
            ["Books", "Favourites", "Main menu"]
        )

    # --------------------------------------------------
    # MENU INPUT TESTS
    # --------------------------------------------------

    @patch("builtins.input", return_value="1")
    def test_get_menu_choice_returns_valid_choice(self, mock_input):
        """Test that a valid menu choice is returned."""

        choice = self.ui.get_menu_choice(self.ui.main_menu)

        self.assertEqual(choice, 1)

    @patch("builtins.input", return_value="0")
    def test_get_menu_choice_returns_zero(self, mock_input):
        """Test that zero is accepted as an exit choice."""

        choice = self.ui.get_menu_choice(self.ui.main_menu)

        self.assertEqual(choice, 0)

    @patch("builtins.input", side_effect=["invalid", "3", "2"])
    def test_get_menu_choice_rejects_invalid_input(self, mock_input):
        """Test that invalid input is rejected before accepting a valid choice."""

        with patch("sys.stdout", new=StringIO()) as output:
            choice = self.ui.get_menu_choice(self.ui.main_menu)

        self.assertEqual(choice, 2)
        self.assertIn("Please enter a valid number.", output.getvalue())
        self.assertIn("Please choose a number", output.getvalue())

    # --------------------------------------------------
    # SEARCH INPUT TESTS
    # --------------------------------------------------

    @patch("builtins.input", side_effect=["   ", "The Hobbit"])
    def test_get_search_term_rejects_empty_input(self, mock_input):
        """Test that an empty search term is rejected."""

        with patch("sys.stdout", new=StringIO()) as output:
            search_term = self.ui.get_search_term()

        self.assertEqual(search_term, "The Hobbit")
        self.assertIn("Search term cannot be empty.", output.getvalue())

    @patch("builtins.input", return_value="  Dune  ")
    def test_get_search_term_removes_whitespace(self, mock_input):
        """Test that whitespace is removed from a search term."""

        search_term = self.ui.get_search_term()

        self.assertEqual(search_term, "Dune")

    # --------------------------------------------------
    # BOOK SELECTION TESTS
    # --------------------------------------------------

    @patch("builtins.input", return_value="1")
    def test_get_book_choice_returns_selected_book(self, mock_input):
        """Test that the correct book is returned."""

        selected_book = self.ui.get_book_choice(self.books)

        self.assertIs(selected_book, self.book_one)

    @patch("builtins.input", return_value="2")
    def test_get_book_choice_returns_second_book(self, mock_input):
        """Test that selecting the second book returns the second object."""

        selected_book = self.ui.get_book_choice(self.books)

        self.assertIs(selected_book, self.book_two)

    @patch("builtins.input", return_value="0")
    def test_get_book_choice_returns_none_when_user_goes_back(self, mock_input):
        """Test that zero returns None."""

        selected_book = self.ui.get_book_choice(self.books)

        self.assertIsNone(selected_book)

    @patch.object(Console, "pause")
    def test_get_book_choice_returns_none_when_no_books_exist(self, mock_pause):
        """Test that an empty book list returns None."""

        selected_book = self.ui.get_book_choice([])

        self.assertIsNone(selected_book)
        mock_pause.assert_called_once()

    @patch("builtins.input", side_effect=["invalid", "5", "1"])
    def test_get_book_choice_rejects_invalid_input(self, mock_input):
        """Test that invalid book selections are rejected."""

        with patch("sys.stdout", new=StringIO()) as output:
            selected_book = self.ui.get_book_choice(self.books)

        self.assertIs(selected_book, self.book_one)
        self.assertIn("Please enter a valid number.", output.getvalue())
        self.assertIn("Please choose a number", output.getvalue())

    # --------------------------------------------------
    # READING PAGE INPUT TESTS
    # --------------------------------------------------

    @patch("builtins.input", return_value="150")
    def test_get_page_number_returns_valid_page(self, mock_input):
        """Test that a valid page number is returned."""

        page_number = self.ui.get_page_number(300)

        self.assertEqual(page_number, 150)

    @patch("builtins.input", return_value="0")
    def test_get_page_number_returns_none_when_cancelled(self, mock_input):
        """Test that zero cancels page selection."""

        page_number = self.ui.get_page_number(300)

        self.assertIsNone(page_number)

    @patch("builtins.input", side_effect=["-5", "301", "150"])
    def test_get_page_number_rejects_invalid_pages(self, mock_input):
        """Test that negative and excessive page numbers are rejected."""

        with patch("sys.stdout", new=StringIO()) as output:
            page_number = self.ui.get_page_number(300)

        self.assertEqual(page_number, 150)
        self.assertIn("Page number cannot be negative.", output.getvalue())
        self.assertIn("This book only has 300 pages.", output.getvalue())

    @patch("builtins.input", side_effect=["invalid", "100"])
    def test_get_page_number_rejects_non_numeric_input(self, mock_input):
        """Test that non-numeric page input is rejected."""

        with patch("sys.stdout", new=StringIO()) as output:
            page_number = self.ui.get_page_number(300)

        self.assertEqual(page_number, 100)
        self.assertIn("Please enter a valid page number.", output.getvalue())

    # --------------------------------------------------
    # GOOGLE BOOKS DISPLAY TESTS
    # --------------------------------------------------

    def test_display_search_results(self):
        """Test that search results display book titles and authors."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_search_results(self.books)

        displayed_text = output.getvalue()

        self.assertIn("The Hobbit", displayed_text)
        self.assertIn("J.R.R. Tolkien", displayed_text)
        self.assertIn("Dune", displayed_text)
        self.assertIn("Frank Herbert", displayed_text)

    def test_display_search_results_with_no_books(self):
        """Test that an empty search result displays an error."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_search_results([])

        self.assertIn("No books found.", output.getvalue())

    def test_display_book_details(self):
        """Test that book details are displayed correctly."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_book_details(self.book_one)

        displayed_text = output.getvalue()

        self.assertIn("The Hobbit", displayed_text)
        self.assertIn("J.R.R. Tolkien", displayed_text)
        self.assertIn("Current page: 100", displayed_text)
        self.assertIn("Pages: 300", displayed_text)
        self.assertIn("Favourite: Yes", displayed_text)
        self.assertIn("Rating: 4.5/5", displayed_text)

    def test_display_book_details_with_optional_information(self):
        """Test that optional book information can be omitted."""

        book = SimpleNamespace(
            title="Unknown Book",
            authors=[],
            subtitle=None,
            published_date=None,
            page_count=0,
            total_pages=None,
            favourite=False,
            average_rating=None,
            description=None
        )

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_book_details(book)

        displayed_text = output.getvalue()

        self.assertIn("Unknown Book", displayed_text)
        self.assertIn("Unknown author", displayed_text)
        self.assertIn("Favourite: No", displayed_text)
        self.assertNotIn("Rating:", displayed_text)
        self.assertNotIn("Description:", displayed_text)

    # --------------------------------------------------
    # LIBRARY DISPLAY TESTS
    # --------------------------------------------------

    def test_display_library_stats(self):
        """Test that the total number of books is displayed."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_library_stats(self.library)

        self.assertIn("Total books: 2", output.getvalue())

    def test_display_library_stats_when_empty(self):
        """Test that an empty library displays the correct message."""

        empty_library = SimpleNamespace(
            books=[],
            total_books=0
        )

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_library_stats(empty_library)

        self.assertIn(
            "You have no books in your library.",
            output.getvalue()
        )

    def test_display_library_books(self):
        """Test that all library books are displayed."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_library_books(self.library)

        displayed_text = output.getvalue()

        self.assertIn("The Hobbit", displayed_text)
        self.assertIn("Dune", displayed_text)

    def test_display_library_books_when_empty(self):
        """Test that an empty library displays an error."""

        empty_library = SimpleNamespace(
            books=[],
            total_books=0
        )

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_library_books(empty_library)

        self.assertIn("Your library is empty.", output.getvalue())

    def test_display_favourites(self):
        """Test that only favourite books are displayed."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_favourites(self.library)

        displayed_text = output.getvalue()

        self.assertIn("The Hobbit", displayed_text)
        self.assertNotIn("Dune", displayed_text)

    def test_display_favourites_when_empty(self):
        """Test that a library without favourites displays a message."""

        empty_favourites_library = SimpleNamespace(
            books=[self.book_two],
            total_books=1
        )

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_favourites(empty_favourites_library)

        self.assertIn(
            "You haven't added any favourite books yet.",
            output.getvalue()
        )

    # --------------------------------------------------
    # READING PROGRESS TESTS
    # --------------------------------------------------

    def test_display_reading_progress(self):
        """Test that reading progress is calculated correctly."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_reading_progress(self.book_one)

        displayed_text = output.getvalue()

        self.assertIn("Current page: 100", displayed_text)
        self.assertIn("Total pages: 300", displayed_text)
        self.assertIn("Progress: 33.3%", displayed_text)

    def test_display_reading_progress_without_total_pages(self):
        """Test that progress is not calculated without a page total."""

        book = SimpleNamespace(
            title="Unknown Book",
            page_count=10,
            total_pages=None
        )

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_reading_progress(book)

        self.assertIn(
            "Page count information is unavailable",
            output.getvalue()
        )

    # --------------------------------------------------
    # MESSAGE TESTS
    # --------------------------------------------------

    def test_display_message(self):
        """Test that a general message is displayed."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_message("Hello LeafMark")

        self.assertIn("Hello LeafMark", output.getvalue())

    def test_display_success_message(self):
        """Test that a success message uses the green colour."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_success_message("Book added")

        displayed_text = output.getvalue()

        self.assertIn("Book added", displayed_text)
        self.assertIn(self.ui.GREEN, displayed_text)

    def test_display_error_message(self):
        """Test that an error message uses the red colour."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_error_message("Something went wrong")

        displayed_text = output.getvalue()

        self.assertIn("Something went wrong", displayed_text)
        self.assertIn(self.ui.RED, displayed_text)

    def test_display_warning_message(self):
        """Test that a warning message uses the yellow colour."""

        with patch("sys.stdout", new=StringIO()) as output:
            self.ui.display_warning_message("Warning")

        displayed_text = output.getvalue()

        self.assertIn("Warning", displayed_text)
        self.assertIn(self.ui.YELLOW, displayed_text)

    # --------------------------------------------------
    # TERMINAL TESTS
    # --------------------------------------------------

    @patch("ui.console.subprocess.run")
    def test_clear_console(self, mock_run):
        """Test that the terminal clear command is executed."""

        self.ui.clear_console()

        mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
