from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(
        min_length=1, max_length=100, description="The description of the book"
    )
    rating: int = Field(gt=0, lt=6)
    test_title: Optional[str] = Field(
        description="test field", alias="testTitle", default=""
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Harry Potter",
                    "author": "J.K. Rowling",
                    "description": "A book about a boy who goes to Hogwarts",
                    "rating": 5,
                }
            ],
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Ben", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "Ben", "A great book!", 5),
    Book(3, "Mastering Endpoints", "Ben", "A awesome book!", 5),
    Book(4, "HP1", "AuthorOne", "Book Description", 2),
    Book(5, "HP2", "AuthorTwo", "Book Description", 3),
    Book(6, "HP3", "AuthorThree", "Book Description", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book.id
