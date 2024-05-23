from datetime import datetime, timedelta
import random

class User:

    def __init__(self, name, dob):
        self.name = name
        self.dob = dob
        self.borrowed_books = []
        self.library_id = self.generate_lib_id()

    def generate_lib_id(self):
        new_id = random.randint(1, 1000)
        return new_id
    
    def borrow_book(self, book, date):
        self.borrowed_books.append({"book": book, "date_borrowed": date})

    def books_borrowed(self):
        return self.borrowed_books
    
    