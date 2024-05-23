import book



class Author:

    def __init__(self, name, biography):
        self.name = name
        self.biography = biography
        self.books_written = []

    def add_book(self, book):
        self.books_written.append(book)

    def get_books(self):
        return self.books_written  # Returning the list of books written by the author

    def get_details(self):
        return {
            "name": self.name,
            "biography": self.biography,
            "books_written": [book.get_title() for book in self.books_written]
        }