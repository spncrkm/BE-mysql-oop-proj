from library import Library
from author import Author
import datetime
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error


db_name = "library_management_system"
user = "root"
password = ""
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

def display_main_menu():
    print("\nWelcome to the Library Management System!")
    print("Main Menu:")
    print("1. Book Operations")
    print("2. User Operations")
    print("3. Author Operations")
    print("4. Genre Operations")
    print("5. Check Overdue Books")
    print("6. Quit")
    return input("Select an option (1-6): ")

def display_book_menu():
    print("\nBook Operations:")
    print("1. Add a new book")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Search for a book")
    print("5. Display all books")
    print("6. Back to main menu")
    return input("Select an option (1-6): ")

def display_user_menu():
    print("\nUser Operations:")
    print("1. Add a new user")
    print("2. View user details")
    print("3. Display all users")
    print("4. Back to main menu")
    return input("Select an option (1-4): ")

def display_author_menu():
    print("\nAuthor Operations:")
    print("1. Add a new author")
    print("2. View author details")
    print("3. Display all authors")
    print("4. Back to main menu")
    return input("Select an option (1-4): ")

def display_genre_menu():
    print("\nGenre Operations:")
    print("1. Add a new genre")
    print("2. View genre details")
    print("3. Display all genres")
    print("4. Back to main menu")
    return input("Select an option (1-4): ")


def book_operations(library):
    while True:
        choice = display_book_menu()
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            library.add_book(title, author, isbn)
        elif choice == '2':
            library_id = input("Enter your library ID: ")
            isbn = input("Enter book ISBN: ")
            library.check_out_book(library_id, isbn)
        elif choice == '3':
            library_id = input("Enter your library ID: ")
            isbn = input("Enter book ISBN: ")
            library.return_book(library_id, isbn)
        elif choice == '4':
            isbn = input("Enter book ISBN: ")
            book = library.books.get(isbn)
            if book:
                print(f"Title: {book.get_title()}, Author: {book.get_author()}, ISBN: {book.get_isbn()}")
            else:
                print("Book not found.")
        elif choice == '5':
            for isbn, book in library.books.items():
                print(f"Title: {book.get_title()}, Author: {book.get_author()}, ISBN: {isbn}")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


def user_operations(library):
    while True:
        choice = display_user_menu()
        if choice == '1':
            name = input("Enter user name: ")
            dob = input("Enter user date of birth (YYYY-MM-DD): ")
            email = input("Enter user email: ")
            library_id = library.add_user(name, dob, email)
            print(f"User added with library ID: {library_id}")
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                new_user = (name, dob, email)

                query = "INSERT INTO Users(name, dob, email) VALUES (%s, %s, %s)"
                cursor.execute(query, new_user)
                conn.commit()
                print("New user added successfully!")
            except Error as e:
                print(f"Error as {e}")
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
        elif choice == '2':
            library_id = input("Enter user library ID: ")
            user = library.users.get(library_id)
            if user:
                print(f"Name: {user.name}, DOB: {user.dob}, Email: {user.email}, Borrowed Books: {user.books_borrowed()}")
            else:
                print("User not found.")
        elif choice == '3':
            for user in library.users.values():
                print(f"Name: {user.name}, DOB: {user.dob}, Email: {user.email}, Library ID: {user.library_id}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
        
            

def overdue_books(library):
    overdue_books = Library.check_overdue_books()
    if overdue_books:
        print("\nOverdue Books:")
        for entry in overdue_books:
            user = library.users[entry["user_id"]]
            book = entry["book"]
            due_date = entry["due_date"]
            print(f"User: {user.name}, Book: {book.get_title()}, Due Date: {due_date}")
    else:
        print("\nNo overdue books.")


def author_operations(library):
    while True:
        choice = display_author_menu()
        if choice == '1':
            name = input("Enter author name: ")
            biography = input("Enter author biography: ")
            author = Author(name, biography)
            library.authors[name] = author
            print("Author added successfully.")
        elif choice == '2':
            name = input("Enter author name: ")
            author = library.authors.get(name)
            if author:
                print(f"Name: {author.name}, Biography: {author.biography}, Books Written: {author.get_books()}")
            else:
                print("Author not found.")
        elif choice == '3':
            for author in library.authors.values():
                print(f"Name: {author.name}, Biography: {author.biography}, Books Written: {author.get_books()}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


def genre_operations(library):
    while True:
        choice = display_genre_menu()
        if choice == '1':
            name = input("Enter genre name: ")
            description = input("Enter genre description: ")
            category = input("Enter genre category (optional): ")
            library.add_genre(name, description, category)
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "INSERT INTO genres(name, description) VALUES (%s, %s)"
            cursor.execute(query)
            conn.commit()

            cursor.close()
            conn.close()

        elif choice == '2':
            name = input("Enter genre name: ")
            genre = library.get_genre_details(name)
            if genre:
                print(f"Name: {genre['name']}, Description: {genre['description']}, Category: {genre['category']}")
        elif choice == '3':
            library.display_all_genres()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    library = Library()

    while True:
        choice = display_main_menu()
        if choice == '1':
            book_operations(library)
        elif choice == '2':
            user_operations(library)
        elif choice == '3':
            author_operations(library)
        elif choice == '4':
            genre_operations(library)
        elif choice == '5':
            library.check_overdue_books()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




## just for copy and pasting purposes to input into CLI
# author: J.K. Rowling {" Harry Potter and the Sorcerer's Stone " 978054069670,
#                       " Harry Potter and the Chamber of Secrets " 9788532530554,
#                       " Harry Potter and the Prisoner of Azkaban " 9780605953208,
#                       " Harry Potter and the Goblet of Fire " 9788893819930
#                       }
# author Stephen King {" It ",
#                      " The Shining" 9780385121675,
#                      " Pet Sematary" 9780385182447,
#                      " Shawshank Redemption" 9785271219290,
#                      " The Green Mile" 9788401485060
#                      }

## I also attempted to implement to check for overdue books within the library.py under method check_out_book
# to set the date of when they check out to the user then the check_overdue_books method under the Library
# class as well for it to check if it has been over 30 days and it will be appended in the overdue_books list 
# within the same method