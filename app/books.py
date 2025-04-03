#uvicorn books:app --reload

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    isbn: str
    title: str
    publish_year: int

books_list = [Book(id="1", isbn="1234567890123", title="Súper libro de Física", publish_year=2020),
         Book(id="2", isbn="0987654321098", title="Robots e imperio", publish_year=1985),
         Book(id="3", isbn="4564564564564", title="De la tierra a la luna", publish_year=1980)]

@app.get("/books")
async def books():
    return books_list

@app.get("/book/{id}")
async def book(id: int):
    return get_book(id)

@app.post("/book/")
async def book(book: Book):
    if (type(get_book(book.id)) == Book):
        return {"error": "El libro ya existe."}
    else:
        books_list.append(book)
        return book

@app.put("/book/")
async def book(book: Book):
    for i, saved_book in enumerate(books_list):
        if (saved_book.id == book.id):
            books_list[i] = book
            return book
    return {"error": "Libro no existente."}

@app.delete("/book/{id}")
async def book(id: int):
    for i, saved_book in enumerate(books_list):
        if (saved_book.id == id):
            del books_list[i]
            return True
    return {"error": "Libro no existente."}

def get_book(id: int):
    filtered_books = filter(lambda b: b.id == id, books_list)
    try:
        return list(filtered_books)[0]
    except:
        return {"error": "Libro no existente."}