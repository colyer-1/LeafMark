# LeafMark

LeafMark is a Python-based personal book library application that integrates with the Google Books API.

It allows users to search for books, build a personal library and track their reading activity.

LeafMark is being developed to support multiple ways of interacting with the same application, including:

- **Console application** – an interactive command-line interface.
- **Web application** – a browser-based interface (planned).
- **Future interfaces** – additional ways to access and manage a personal library as the project develops.

The goal is to maintain shared application functionality across these different interfaces, avoiding unnecessary duplication and allowing LeafMark to grow into a flexible, full-stack application.

## Features

- Search for books using the Google Books API.
- View book information and details.
- Add and remove books from a personal library.
- Prevent duplicate books using Google Books IDs.
- Persist library data using SQLite.
- Track reading progress by updating the current page.
- Calculate reading progress.
- Mark books as favourites.
- View library statistics and favourite books.

## Technologies

- **Python** – application development.
- **SQLite** – persistent data storage.
- **Requests** – HTTP requests to the Google Books API.
- **python-dotenv** – environment variable management.
- **unittest** – automated testing.
- **Git and GitHub** – version control.

## Project structure

```text
LeafMark/
├── console/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── book.py
│   └── library.py
├── services/
│   ├── database.py
│   └── google_books_client.py
├── tests/
│   ├── test_book.py
│   ├── test_console.py
│   ├── test_database.py
│   ├── test_google_books_client.py
│   ├── test_google_books_conversion.py
│   └── test_library.py
├── ui/
│   └── console.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/colyer-1/LeafMark.git
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

From the project root, launch the console application:

```bash
python -m console.main
```

The SQLite database and required tables are initialised when the application starts.

## Running tests

LeafMark uses Python's built-in `unittest` framework.

Run the complete test suite:

```bash
python -m unittest discover -v
```

## Architecture

LeafMark uses separation of responsibilities to keep the application organised.

- `console/` – contains the command-line application's entry point.
- `models/` – represents books and manages library behaviour.
- `services/` – handles database operations and communication with Google Books.
- `ui/` – manages command-line interaction and presentation.
- `tests/` – contains automated tests.

The console interface uses shared models and services rather than implementing its own application logic.

The project is intended to support multiple interfaces that interact with the same underlying application functionality and data.

## Development goals

LeafMark is an ongoing software development project.

Planned improvements include:

- Introducing Django as a web application backend.
- Developing a browser-based user interface.
- Reusing existing application functionality where appropriate.
- Adding user accounts and authentication.
- Exploring additional interfaces and ways to access the application.
- Deploying the application.

The long-term goal is to develop LeafMark into a multi-interface application, where users can access the same personal library through different platforms while sharing the underlying application logic, services and database.