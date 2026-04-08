from time import perf_counter
from typing import Annotated, Optional

from fastapi import BackgroundTasks, Cookie, FastAPI, Form, Header, Path, Query, Request, Response

from models.models import FormData, Book
from routes.auth import get_profile
from routes.login import login
from routes.signup import signup
from routes.books import (
    get_books,
    get_product_shop,
    get_product_shop_by_id,
    add_book,
    delete_book,
    update_book,
    test_query
)

app = FastAPI()


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    elapsed = perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    print(f"{request.method} {request.url.path} completed in {elapsed:.4f}s")
    return response


@app.post("/login")
def login_endpoint(
    data: Annotated[FormData, Form()],
    response: Response,
    background_tasks: BackgroundTasks
):
    return login(data, response, background_tasks)


@app.post("/signup")
def signup_endpoint(
    data: Annotated[FormData, Form()],
    response: Response,
    background_tasks: BackgroundTasks
):
    return signup(data, response, background_tasks)


@app.get("/profile")
def get_profile_endpoint(session_id: Optional[str] = Cookie(None)):
    return get_profile(session_id)


@app.get("/")
def root():
    return {"message": "Hello, World! welcome to the bookStore API"}


@app.get("/books/")
def get_books_endpoint(x_token: str = Header(...)):
    return get_books(x_token)


@app.get("/shops/")
def get_product_shop_endpoint():
    return get_product_shop()


@app.get("/shops/{book_id}")
def get_product_shop_by_id_endpoint(
    book_id: Annotated[int, Path(title="The ID of the book to retrieve", ge=1)]
):
    return get_product_shop_by_id(book_id)


@app.post("/add-book")
def add_book_endpoint(book: Book, background_tasks: BackgroundTasks):
    return add_book(book, background_tasks)


@app.delete("/delete/{book_id}")
def delete_book_endpoint(book_id: int):
    return delete_book(book_id)


@app.put("/update/{book_id}")
def update_book_endpoint(book_id: int, book: Book):
    return update_book(book_id, book)


@app.get("/test/")
async def test_query_endpoint(
    q: Annotated[str | None, Query(title="title of the book", alias="item-q", min_length=3)] = None
):
    return await test_query(q)