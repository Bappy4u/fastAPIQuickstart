from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated
from uuid import uuid4

app = FastAPI()


items = [
    {"id": 1, "title": "Book A", "price": 10.99, "author": "Author A", "description": "A great book about A"},
    {"id": 2, "title": "Book B", "price": 15.99, "author": "Author B", "description": "A great book about B"},
    {"id": 3, "title": "Book C", "price": 8.99, "author": "Author C", "description": "A great book about C"}
]

class Book(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None

@app.get("/")
def root():
    return {"message": "Hello, World! welcome to the bookStore API"}

@app.get("/shops/")
def get_product_shop():
    return {"Books": items}


@app.get("/shops/{book_id}")
def get_product_shop(book_id: int):
    for item in items:
        if item["id"] == book_id:
            return {"Book": item}
    return {"message": "Book not found"}


@app.post("/add-book")
def add_book(book: Book):
    book_dict = book.model_dump()
    book_dict["id"] = str(uuid4())
    items.append(book_dict)
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
async def test_query(q: Annotated[ str | None, Query(min_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results