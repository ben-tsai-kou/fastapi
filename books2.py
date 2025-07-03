from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(
        min_length=1, max_length=100, description="The description of the book"
    )
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1900, lt=2025, max_length=4)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Harry Potter",
                    "author": "J.K. Rowling",
                    "description": "A book about a boy who goes to Hogwarts",
                    "rating": 5,
                    "published_date": 2025,
                }
            ],
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Ben", "A very nice book!", 5, 2025),
    Book(2, "Be Fast with FastAPI", "Ben", "A great book!", 5, 2025),
    Book(3, "Mastering Endpoints", "Ben", "A awesome book!", 5, 2024),
    Book(4, "HP1", "AuthorOne", "Book Description", 2, 2024),
    Book(5, "HP2", "AuthorTwo", "Book Description", 3, 2024),
    Book(6, "HP3", "AuthorThree", "Book Description", 1, 2023),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/published", status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date: int = Query(gt=1900, le=2025)):
    print(type(publish_date))
    books_to_return = []
    for book in BOOKS:
        if book.published_date == publish_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/rating", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(
    book_id: int = Path(description="The ID of the book you want to read", gt=0)
):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book.id


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int = Path(description="The ID of the book you want to delete", gt=0)
):
    book_to_delete = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_to_delete = True
            break
    if not book_to_delete:
        raise HTTPException(status_code=404, detail="Book not found")
