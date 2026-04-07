from time import perf_counter
from uuid import uuid4

from fastapi import BackgroundTasks, Cookie, FastAPI, Form, Header, HTTPException, Path, Query, Request, Response, status
from pydantic import BaseModel
from typing import Annotated, Optional

app = FastAPI()


def send_email(email: str, subject: str, body: str) -> None:
    print(f"Sending email to {email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("Email sent successfully")


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    elapsed = perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    print(f"{request.method} {request.url.path} completed in {elapsed:.4f}s")
    return response


items = [
    {"id": 1, "title": "Book A", "price": 10.99, "author": "Author A", "description": "A great book about A"},
    {"id": 2, "title": "Book B", "price": 15.99, "author": "Author B", "description": "A great book about B"},
    {"id": 3, "title": "Book C", "price": 8.99, "author": "Author C", "description": "A great book about C"}
]

class FormData(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(data: Annotated[FormData, Form()], response: Response, background_tasks: BackgroundTasks):
    response.set_cookie(key="session_id", value="abc123")
    background_tasks.add_task(
        send_email,
        email=f"{data.username}@example.com",
        subject="Welcome to BookStore",
        body=f"Hi {data.username}, you have successfully logged in."
    )
    return {"message": "Logged in"}

@app.get("/profile")
def get_profile(session_id: Optional[str] = Cookie(None)):
    if session_id != "abc123":
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {"message": "Welcome user"}

class Book(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "The Great Gatsby",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "author": "John Doe",
                }
            ]
        }
    }

@app.get("/")
def root():
    return {"message": "Hello, World! welcome to the bookStore API"}

@app.get("/books/")
def get_books(x_token: str = Header(...)):
    if x_token != "secret123":
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"message": "Access granted", "books": []}

@app.get("/shops/")
def get_product_shop():
    return {"Books": items}


@app.get("/shops/{book_id}")
def get_product_shop(book_id: Annotated[int, Path(title="The ID of the book to retrieve", ge=1)],):
    book = next((item for item in items if item["id"] == book_id), None)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error": "BookNotFound",
            "message": f"Book with id {book_id} not found"
        })
    return {"book": book}


@app.post("/add-book")
def add_book(book: Book, background_tasks: BackgroundTasks):
    book_dict = book.model_dump()
    book_dict["id"] = str(uuid4())
    items.append(book_dict)
    background_tasks.add_task(
        send_email,
        email="admin@bookstore.com",
        subject="New book added",
        body=f"The book '{book.title}' was added to inventory."
    )
    return {"message": "Book created successfully", "book": book_dict}


@app.delete("/delete/{book_id}")
def delete_book(book_id: int):
    for item in items:
        if item["id"] == book_id:
            print(f"Deleting book with id: {book_id}")
            items.remove(item)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}


@app.put("/update/{book_id}")
def update_book(book_id: int, book: Book):
    for item in items:
        if item["id"] == book_id:
            item.update(book.model_dump())
            return {"message": "Book updated successfully", "book": item}
    return {"message": "Book not found"}


@app.get("/test/")
async def test_query(q: Annotated[ str | None, Query(title="title of the book", alias="item-q", min_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results