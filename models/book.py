class Book:
    """
    Represents an individual book in the Leafmark application.
    Stores book information and tracks reading progress.
    """

    def __init__(
            self,
            id,
            title,
            authors,
            total_pages=None,
            subtitle=None,
            description=None,
            published_date=None,
            image_url=None,
            average_rating=None
    ):
        # Store required book information.
        self._id = id
        self._title = title
        self._authors = authors

        # Store optional book information.
        self._subtitle = subtitle
        self._description = description
        self._total_pages = total_pages
        self._published_date = published_date
        self._image_url = image_url
        self._average_rating = average_rating

        # Initialise reading progress for a new book.
        self._page_count = 0
        self.is_finished = False
        self._favourite = False

    # Read-only properties for accessing book information.
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title

    @property
    def subtitle(self):
        return self._subtitle

    @property
    def authors(self):
        return self._authors

    @property
    def description(self):
        return self._description

    @property
    def total_pages(self):
        return self._total_pages

    @property
    def published_date(self):
        return self._published_date

    @property
    def image_url(self):
        return self._image_url

    @property
    def average_rating(self):
        return self._average_rating

    # Calculate reading progress as a percentage.
    # Return None if the total page count is unknown.
    @property
    def progress(self):
        if self._total_pages is None or self._total_pages == 0:
            return None

        return self._page_count / self._total_pages * 100

    # Allow access to the current page count.
    @property
    def page_count(self):
        return self._page_count

    # Determine reading status from the current page count.
    @property
    def reading_status(self):
        if self.is_finished:
            return "Finished"
        elif self.page_count > 0:
            return "In progress"
        else:
            return "Not started yet"

    @property
    def favourite(self):
        return self._favourite

    # Validate and update reading progress.
    @page_count.setter
    def page_count(self, value):

        # Ensure page count is an integer, excluding booleans.
        if type(value) is not int:
            raise TypeError("Page count must be an integer")

        # Ensure page count is within the valid page range.
        if value < 0:
            raise ValueError("Page count cannot be negative")

        # Only validate against total pages when known.
        if self._total_pages is not None and value > self._total_pages:
            raise ValueError(
                "Page count must be between 0 and total pages"
            )

        # Update reading progress.
        self._page_count = value

        # Update completion status when total pages are known.
        self.is_finished = (
            self._total_pages is not None
            and self._total_pages > 0
            and self._page_count == self._total_pages
        )

    @favourite.setter
    def favourite(self, bool):
        self._favourite = bool   
