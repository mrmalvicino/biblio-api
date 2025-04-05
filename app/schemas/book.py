def book_schema(book) -> dict:
    return {
        "id": str(book["_id"]),
        "isbn": book["isbn"],
        "title": book["title"],
        "publish_year": book["publish_year"]
    }

def books_schema(books) -> list:
    return [book_schema(b) for b in books]