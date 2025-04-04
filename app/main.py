from fastapi import FastAPI
from routers import books, authors
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(books.router)
app.include_router(authors.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")