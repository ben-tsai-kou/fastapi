from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Category One"},
    {"title": "Title Two", "author": "Author Two", "category": "Category Two"},
    {"title": "Title Three", "author": "Author Three", "category": "Category Three"},
    {"title": "Title Four", "author": "Author Four", "category": "Category Four"},
    {"title": "Title Five", "author": "Author Five", "category": "Category Five"},
    {"title": "Title Six", "author": "Author Six", "category": "Category Six"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS
