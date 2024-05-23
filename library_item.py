class LibraryItem:
    def __init__(self, title, category=None):
        self.title = title
        self.category = category

    def get_title(self):
        return self.title
    
    def get_category(self):
        return self.category

    def set_title(self, title):
        self.title = title

    def set_category(self, category):
        self.category = category