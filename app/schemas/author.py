def author_schema(author) -> dict:
    return {
        "id": str(author["_id"]),
        "isni": author["isni"],
        "name": author["name"],
        "birth_year": author["birth_year"],
        "books": [str(b) for b in author.get("books", [])]
    }

def authors_schema(authors) -> list:
    return [author_schema(a) for a in authors]