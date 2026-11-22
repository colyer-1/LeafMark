
# Import os so we can access environment variables.
import os

# Import requests so we can send HTTP requests to Google Books.
import requests

# Import our own Book class.
# This allows us to convert Google Books API data into Book objects.
from models.book import Book


class GoogleBooksClient:
    """
    Handles communication with the Google Books API.

    Searches for books and converts the API responses
    into Book objects that our application can use.
    """

    # The base URL for the Google Books volumes endpoint.
    # We store this as a class attribute because it is shared
    # by every instance of GoogleBooksClient.
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def __init__(self):
        # Retrieve the Google Books API key from the environment.
        # Keeping the key outside the source code means we don't
        # have to expose sensitive credentials in our project.
        self.api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    def query_book(self, search_term, qty=10):
        """
        Search Google Books using a search term.

        Args:
            search_term: The title, author or keywords to search for.
            qty: The maximum number of results to request.

        Returns:
            A list of Book objects.
        """

        # Prepare the search parameters.
        # Google Books uses 'q' for the search query,
        # 'key' for our API key and 'maxResults' for the result limit.
        # Google Books allows a maximum of 40 results per request.
        params = {
            "q": search_term,
            "key": self.api_key,
            "maxResults": min(qty, 40)
        }

        # Send an HTTP GET request to the Google Books API.
        # The params dictionary is automatically added to the URL
        # as query string parameters.
        response = requests.get(
            self.BASE_URL,
            params=params
        )

        # Check whether the HTTP request was successful.
        # If Google returns an error status, such as 404 or 429,
        # requests will raise an HTTPError.
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary.
        data = response.json()

        # Create an empty list to store our Book objects.
        books = []

        # Loop through the search results returned by Google.
        # If the response doesn't contain an 'items' key,
        # use an empty list instead.
        for item in data.get("items", []):

            try:
                # Convert the complete Google Books item into
                # an instance of our own Book class.
                book = self._convert_to_book(item)

                # Add the Book object to our collection.
                books.append(book)

            except ValueError:
                # Skip results that don't contain a valid title.
                continue

        # Return the collection of Book objects to the caller.
        return books

    def _convert_to_book(self, item):
        """
        Convert a complete Google Books API item into a Book object.

        Args:
            item: A dictionary containing the complete book information
                  returned by the Google Books API.

        Returns:
            A Book object.
        """

        # Extract the Google Books ID.
        # The ID is stored outside the volumeInfo dictionary.
        book_id = item.get("id")

        # Extract the book's volume information.
        volume_info = item.get("volumeInfo", {})

        # Extract the title from the API response.
        # A title is required for a valid Book object.
        title = volume_info.get("title")

        # Reject the result if the title is missing or empty.
        if not title:
            raise ValueError("Book must have a title")

        # Extract the authors.
        # Authors are optional, so use an empty list if unavailable.
        authors = volume_info.get("authors", [])

        # Extract optional book information.
        # The .get() method returns None when a key is missing.
        subtitle = volume_info.get("subtitle")
        description = volume_info.get("description")
        page_count = volume_info.get("pageCount")
        published_date = volume_info.get("publishedDate")
        average_rating = volume_info.get("averageRating")

        # Extract the image information.
        # imageLinks might not exist in the API response,
        # so default to an empty dictionary.
        image_links = volume_info.get("imageLinks", {})

        # Get the thumbnail URL if one is available.
        image_url = image_links.get("thumbnail")

        # Create an instance of our own Book class.
        # We use named arguments to make it clear which
        # API values are being passed into which Book attributes.
        book = Book(
            id=book_id,
            title=title,
            authors=authors,
            total_pages=page_count,
            subtitle=subtitle,
            description=description,
            published_date=published_date,
            image_url=image_url,
            average_rating=average_rating
        )

        # Return the completed Book object.
        return book
