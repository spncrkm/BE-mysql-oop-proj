from library_item import LibraryItem

class Book(LibraryItem):

    def __init__(self, title, author, isbn, category = None):
        super().__init__(title, category)
        self.__author = author
        self.__isbn = isbn
        self.__is_available = True
    
    def get_author(self):
        return self.__author
    
    def get_isbn(self):
        return self.__isbn
    
    def check_out(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False
    
    def return_book(self):
        self.__is_available = True



