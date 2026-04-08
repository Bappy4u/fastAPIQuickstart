from typing import Annotated

from fastapi import BackgroundTasks, Header, HTTPException, Path, Query, status
from uuid import uuid4

from models.models import Book
from data.data import items
from utils.email_utils import send_email


def get_books(x_token: str = Header(...)):
    if x_token != "secret123":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": "Access granted", "books": []}


def get_product_shop():
    return {"Books": items}


def get_product_shop_by_id(book_id: Annotated[int, Path(title="The ID of the book to retrieve", ge=1)]):
    book = next((item for item in items if item["id"] == book_id), None)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error": "BookNotFound",
            "message": f"Book with id {book_id} not found"
        })
    return {"book": book}


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


def delete_book(book_id: int):
    for item in items:
        if item["id"] == book_id:
            print(f"Deleting book with id: {book_id}")
            items.remove(item)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}


def update_book(book_id: int, book: Book):
    for item in items:
        if item["id"] == book_id:
            item.update(book.model_dump())
            return {"message": "Book updated successfully", "book": item}
    return {"message": "Book not found"}


async def test_query(q: Annotated[ str | None, Query(title="title of the book", alias="item-q", min_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results