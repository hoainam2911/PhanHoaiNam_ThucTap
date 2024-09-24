import json

class Book:
    def __init__(self,id,title,description,author):
        self.title = title
        self.author = author
        self.id = id
        self.description = description
    
    def __str__(self):
        return f"'{self.title}'by {self.author.name}"
    
    def to_dict(self):
        return{
            "title": self.title,
            "author": self.author,
            "id": self.id,
            "description": self.description
        }
    
    @staticmethod
    def from_dict(data):
        author = Author(data["author"])
        return Book(data["title","id","description"], author)
    
class Author:
    def __init__(self,name):
        self.name = name
    
    def __str__(self):
        return self.name
    
class Library:
    def __init__(self):
        self.books = []
        self.filename = "library_data.json"
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                if file.read(1);
