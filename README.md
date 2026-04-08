# BookStore API

A FastAPI application for managing a bookstore with authentication and book management features.

## Project Structure

```
BookStore/
├── main.py                 # Application entry point with FastAPI app and middleware
├── models/
│   ├── __init__.py
│   └── models.py          # Pydantic models (FormData, Book)
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Profile routes (get_profile)
│   ├── login.py           # Login authentication routes
│   ├── signup.py          # User registration routes
│   └── books.py           # Book management routes (CRUD operations)
├── utils/
│   ├── __init__.py
│   └── email_utils.py     # Email utility functions
├── data/
│   ├── __init__.py
│   └── data.py            # In-memory data storage
├── requirements.txt        # Python dependencies
└── README.md
```

## Features

- User authentication with session cookies
- Book CRUD operations (Create, Read, Update, Delete)
- Background email notifications
- Request timing middleware
- Query parameter validation

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv env
   ```

2. Activate the virtual environment:
   - Windows: `env\Scripts\activate`
   - Linux/Mac: `source env/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Welcome message
- `POST /signup` - User registration
- `POST /login` - User login
- `GET /profile` - Get user profile (requires session cookie)
- `GET /books/` - Get books (requires header token)
- `GET /shops/` - Get all books in shop
- `GET /shops/{book_id}` - Get specific book by ID
- `POST /add-book` - Add a new book
- `PUT /update/{book_id}` - Update a book
- `DELETE /delete/{book_id}` - Delete a book
- `GET /test/` - Test query parameters
