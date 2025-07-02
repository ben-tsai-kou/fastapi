from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "AuthorOne", "category": "science"},
    {"title": "Title Two", "author": "AuthorTwo", "category": "science"},
    {"title": "Title Three", "author": "AuthorThree", "category": "history"},
    {"title": "Title Four", "author": "AuthorFour", "category": "math"},
    {"title": "Title Five", "author": "AuthorFive", "category": "math"},
    {"title": "Title Six", "author": "AuthorSix", "category": "math"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_author(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return
