# LeafMark

A Python-based personal book library application that integrates with the Google Books API.

LeafMark allows users to search for books, build a personal library and keep track of their reading activity through an interactive command-line interface.

## Features

- Search for books using the Google Books API.
- View book information and details.
- Add and remove books from a personal library.
- Track reading progress by updating the current page.
- Calculate reading progress.
- Mark books as favourites.
- View library statistics and favourite books.

## Technologies

- **Python** — application development.
- **Requests** — HTTP requests to the Google Books API.
- **python-dotenv** — environment variable management.
- **unittest** — automated testing.

## Project structure

```text
LeafMark/
├── models/
│   ├── book.py
│   └── library.py
├── services/
│   └── google_books_client.py
├── tests/
│   ├── test_book.py
│   ├── test_console.py
│   ├── test_google_books_client.py
│   ├── test_google_books_conversion.py
│   └── test_library.py
├── ui/
│   └── console.py
├── main.py
├── requirements.txt
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/HColyer/LeafMark.git
cd LeafMark
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_BOOKS_API_KEY=your_api_key_here
```

Replace the placeholder with your Google Books API key.

Do not commit your `.env` file or share your API key.

### 5. Run LeafMark

```bash
python main.py
```

## Running tests

LeafMark uses Python's built-in `unittest` framework.

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

## Architecture

LeafMark uses a simple separation of responsibilities:

- `models/` — represents books and manages library behaviour.
- `services/` — handles communication with external services such as Google Books.
- `ui/` — manages command-line interaction and presentation.
- `tests/` — contains automated tests.
- `main.py` — coordinates the application.

## Development goals

LeafMark is an ongoing software development project.

Planned improvements include:

- Persistent storage using SQLite.
- A backend API.
- A web-based frontend.
- User accounts and authentication.

The long-term goal is to develop LeafMark from a command-line application into a full-stack web application.