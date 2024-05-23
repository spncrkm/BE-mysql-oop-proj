from library_item import LibraryItem


class Genre(LibraryItem):

    def __init__(self, name, description, category=None):
        super().__init__(name, category)
        self.description = description

    
    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_details(self):
        return {
            "name": self.title,
            "description": self.description,
            "category": self.category
        }