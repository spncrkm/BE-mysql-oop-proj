from book import Book
from user import User
from author import Author
from genre import Genre
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from marshmallow import fields, ValidationError
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error



db_name = "library_management_system"
user = "root"
password = "Emilyalice1001"
host = "localhost"



def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        if conn.is_connected():
            print("Connected to db successfully")
            return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None






class Library:

    def __init__(self):
        self.users = {} # Dictionary to store users with library_id as keys
        self.books = {}  # Dictionary to store books by ISBN as keys
        self.authors = {}  
        self.genres = {}
        self.overdue_books = []


    def add_user(self, name, dob, email):
        new_user = User(name, dob, email)  # User object and generate a library ID
        library_id = new_user.generate_lib_id()  # Generate library ID for the new user
        self.users[library_id] = new_user  # Add user to the library dictionary
        new_user2 = (name, dob, email)
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users(name, dob, email) VALUES (%s, %s, %s)"
        cursor.execute(query, new_user2)
        conn.commit()

        cursor.close()
        conn.close()

        return new_user.library_id  # Return the generated library ID to the new user
        
    
    def check_out_book(self, library_id, isbn):
        user = self.users.get(library_id)
        if not user:
            print("User not found.")
        book = self.books.get(isbn)
        if not book:
            print("Book not found.")
        
        if book.check_out():
            user.borrow_book(book, datetime.now())
            print("Book checked out successfully.")
        else:
            print("Book is not available.")
        

        user_id = library_id
        borrow_date = input("Enter the date borrowed: yyyy-mm-dd")
        isbn = book
        return_date = ""
        borrow_book_info = (user_id, borrow_date, return_date, isbn)
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO borrowed_books(user_id, borrow_date, return_date, isbn) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, borrow_book_info)
        conn.commit()

        cursor.close()
        conn.close()


        
    def return_book(self, library_id, isbn):
        user = self.users.get(library_id) # get the user object based on library ID
        if not user:
            print("User not found.")
            return
        for borrowed_book in user.borrowed_books:
            if borrowed_book["book"].get_isbn() == isbn:
                user.borrowed_books.remove(borrowed_book)
                borrowed_book["book"].return_book()
                print("Book returned successfully.")
                return
        print("Book not found in user's borrowed list.")


    def check_overdue_books(self):
        current_date = datetime.now()
        for user_id, user in self.users.items():
            for borrowed_book in user.borrowed_books:
                date_borrowed = borrowed_book["date_borrowed"]
                due_date = date_borrowed + timedelta(days=30)

                if current_date > due_date:
                    self.overdue_books.append({"user_id": user_id, "book": borrowed_book["book"], "due_date": due_date})
            print(due_date)
        return self.overdue_books
    


    

    def add_book(self, title, author_name, isbn, category=None):
        # Find or create the author
        if author_name in self.authors:
            author = self.authors[author_name]
        else:
            biography = input(f"Enter biography for author {author_name}: ")
            author = Author(author_name, biography)
            self.authors[author_name] = author
        conn = get_db_connection()
        cursor = conn.cursor()
        new_book = (title, author_name, isbn)

        query = "INSERT INTO books(title, author_name, isbn) VALUES (%s, %s, %s)"
        cursor.execute(query, new_book)
        conn.commit()

        cursor.close()
        conn.close()
        

        # # Create and add the book
        # book = Book(title, author_name, isbn, category)
        # self.books[isbn] = book
        # author.add_book(book)

    def get_books_by_author(self, author_name):
        if author_name in self.authors:
            author = self.authors[author_name]
            return author.get_books()
        else:
            return []
        
    def add_genre(self, name, description, category=None):
        if name in self.genres:
            print(f"Genre {name} already exists.")
            return
        genre = Genre(name, description, category)
        self.genres[name] = genre
        print(f"Genre {name} added successfully.")
        genre_name = genre
        genre_details = genre.get_details()
        genre_info = (genre_name, genre_details)
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO genres(genre_name, genre_details) VALUES (%s, %s)"
        cursor.execute(query, genre_info)
        conn.commit()

        cursor.close()
        conn.close()
        

    def get_genre_details(self, name):
        if name in self.genres:
            genre = self.genres[name]
            return genre.get_details()
            
        else:
            print(f"Genre {name} not found.")
            return None 
        
        


    def display_all_genres(self):
        for genre in self.genres.values():
            print(f"Name: {genre.get_name()}, Description: {genre.get_description()}, Category: {genre.get_category()}")
