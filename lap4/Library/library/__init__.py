import json
from user import UserManager
from datetime import datetime
from colorama import Fore, Style, init
from pyfiglet import figlet_format

# Khởi tạo colorama
init(autoreset=True)

class Book:
    def __init__(self, title, author, description, book_id=None, date_added=None, page=None):
        self.title = title
        self.author = author
        self.description = description
        self.book_id = book_id
        self.date_added = date_added or datetime.now().strftime("%Y-%m-%d")
        self.page = page
        
    def __str__(self):
        return f"'{self.title}' by {self.author.name} - Description: {self.description} (ID: {self.book_id}, Added on: {self.date_added}, Page: {self.page})"
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author.name,
            "description": self.description,
            "id": self.book_id,
            "date_added": self.date_added,
            "page": self.page
        }

    @staticmethod
    def from_dict(data):
        author = Author(data["author"])
        return Book(
            title=data["title"],
            author=author,
            description=data["description"],
            book_id=data.get("id"),
            page=data.get("page")
        )

class Author:
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
    
class Library:
    def __init__(self):
        self.book = []
        self.filename = "library_data.json"
        self.load_from_file()
        
    def add_book(self, book):
        title = book.title.strip().lower()
        author_name = book.author.name.strip().lower()
        description = book.description.strip().lower()
        if not title:
            print(Fore.RED + Style.BRIGHT + "Error: Book title cannot be empty.")
            return
        if not author_name:
            print(Fore.RED + Style.BRIGHT + "Error: Author name cannot be empty.")
            return       
        if not description:
            print(Fore.RED + Style.BRIGHT + "Error: Description cannot be empty.")
            return        
        if self.book:
            max_id = max([b.book_id for b in self.book if b.book_id is not None])
            book.book_id = max_id + 1
        else:
            book.book_id = 1
        self.book.append(book)
        print(Fore.GREEN + Style.BRIGHT + f"Added: {book}")
        self.save_to_file()

    def remove_book(self, title):
        title = title.strip().lower()
        for book in self.book:
            if book.title.lower() == title:
                confirm = input(Fore.YELLOW + Style.BRIGHT + f"Are you sure you want to delete the book '{title}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.book.remove(book)
                    print(Fore.GREEN + Style.BRIGHT + f"Removed: {book}")
                    self.save_to_file()
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "Book deletion has been canceled.")
                return
        print(Fore.RED + Style.BRIGHT + f"Book with title '{title}' not found.")
    
    def find_book_by_title(self, title):
        title = title.strip().lower()
        for book in self.book:
            if book.title.lower() == title:
                return book
        return None    
    
    def find_book_by_author(self, author):
        author_name = author.name.strip().lower()
        found_books = [book for book in self.book if book.author.name.lower() == author_name]     
        return found_books
    
    def display_all_books(self):
        if not self.book:
            print(Fore.YELLOW + Style.BRIGHT + "No books in the library.")     
        else:
            print(Fore.BLUE + Style.BRIGHT + "List of books in the library:")
            print(Fore.CYAN +"-" * 140)
            print(Fore.CYAN + Style.BRIGHT + f"{'ID':<10}{'Title':<30}{'Author':<20}{'Description':<60}{'Date Added':<15}{'Page':<6}")
            print(Fore.CYAN +"-" * 140)
            for idx, book in enumerate(self.book, 1):
                print(Fore.WHITE + Style.BRIGHT + f"{book.book_id:<10}{book.title:<30}{book.author.name:<20}{book.description:<60}{book.date_added:<15}{book.page:<6}")
            print(Fore.CYAN +"-" * 140)
            
    def edit_book(self, old_title, new_title, new_author_name, new_description, new_page=None):
        old_title = old_title.strip().lower()
        book = self.find_book_by_title(old_title)
        
        if book:
            if new_title.strip():
                book.title = new_title.strip().lower()
            if new_author_name.strip():
                book.author = Author(new_author_name.strip().lower())
            if new_description.strip():
                book.description = new_description.strip().lower()
            if new_page is not None:
                book.page = new_page          
            print(Fore.GREEN + Style.BRIGHT + f"Updated book: {book}")
            self.save_to_file()
        else:
            print(Fore.RED + Style.BRIGHT + f"Book with title '{old_title}' not found.")

    def save_to_file(self):
        with open(self.filename, 'w') as f:
            data = [book.to_dict() for book in self.book]
            json.dump(data, f, indent=4)
        print(Fore.GREEN + Style.BRIGHT + f"Library data has been saved to {self.filename}.")
        
    def load_from_file(self):
        try:
            with open(self.filename, 'r') as f:
                if f.read(1):
                    f.seek(0)
                    data = json.load(f)
                    self.book = [Book.from_dict(item) for item in data]
                    print(Fore.GREEN + Style.BRIGHT + f"Library data has been loaded from {self.filename}.")
                else:
                    print(Fore.YELLOW + Style.BRIGHT + f"File {self.filename} is empty. Library starts empty.")
                    self.book = []
        except FileNotFoundError:
            print(Fore.RED + Style.BRIGHT + f"File {self.filename} not found. Library starts empty.")
            self.book = []
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"File {self.filename} is not valid JSON. Library starts empty.")
            self.book = []

def main():
    print(Fore.MAGENTA + Style.BRIGHT + figlet_format("Library Management", font="starwars"))
    library = Library()
    user_manager = UserManager()
    
    while True:
        print("\n" + Fore.CYAN + Style.BRIGHT + "=" * 40)
        print(Fore.CYAN + Style.BRIGHT + "Library Management System".center(40))
        print(Fore.CYAN + Style.BRIGHT + "=" * 40)
        print(Fore.WHITE + Style.BRIGHT + "1. Login")
        print(Fore.WHITE + Style.BRIGHT + "2. Register")
        print(Fore.RED + Style.BRIGHT + "3. Exit")
        print(Fore.CYAN + Style.BRIGHT + "=" * 40)
        choice = input(Fore.GREEN +"Enter your choice: ").strip().lower()
        
        match choice:
            case "1":
                username = input(Fore.WHITE +"Enter your username: ").strip().lower()
                password = input(Fore.WHITE +"Enter your password: ").strip()
                if user_manager.login(username, password):
                    break
            
            case "2":
                username = input(Fore.WHITE +"Enter new username: ").strip().lower()
                password = input(Fore.WHITE +"Enter new password: ").strip()
                user_manager.register(username, password)
                
            case "3":
                print(Fore.GREEN + Style.BRIGHT + "Exiting...")
                return
            
            case _:
                print(Fore.RED + Style.BRIGHT + "Invalid choice. Please try again.")
                
    while True:
        print("\n" + Fore.CYAN + Style.BRIGHT + "=" * 40)
        print(Fore.CYAN + Style.BRIGHT + "Library Management".center(40))
        print(Fore.CYAN + Style.BRIGHT + "=" * 40)
        print(Fore.WHITE + Style.BRIGHT + "1. Add book")
        print(Fore.WHITE + Style.BRIGHT + "2. Remove book")
        print(Fore.WHITE + Style.BRIGHT + "3. Find book by title")
        print(Fore.WHITE + Style.BRIGHT + "4. List books by author")
        print(Fore.WHITE + Style.BRIGHT + "5. Display all books")
        print(Fore.WHITE + Style.BRIGHT + "6. Edit book")
        print(Fore.RED + Style.BRIGHT + "7. Logout")
        print(Fore.CYAN + Style.BRIGHT + "=" * 40)
        choice = input(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Enter your choice: ").strip().lower()

        match choice:
            case '1':
                title = input(Fore.CYAN + "Enter book title: ").strip().lower()
                author_name = input(Fore.CYAN + "Enter author name: ").strip().lower()
                description = input(Fore.CYAN + "Enter book description: ").strip().lower()
                page = input(Fore.CYAN + "Enter book page (optional): ").strip()
                page = int(page) if page else None
                book = Book(title=title, author=Author(author_name), description=description, page=page)
                library.add_book(book)
                
            case '2':
                title = input(Fore.CYAN + "Enter book title to remove: ").strip().lower()
                library.remove_book(title)
                
            case '3':
                title = input(Fore.CYAN + "Enter book title to find: ").strip().lower()
                book = library.find_book_by_title(title)
                if book:
                    print(Fore.GREEN + Style.BRIGHT + str(book))
                else:
                    print(Fore.RED + Style.BRIGHT + f"Book with title '{title}' not found.")
                    
            case '4':
                author_name = input(Fore.CYAN + "Enter author name: ").strip().lower()
                author = Author(author_name)
                books = library.find_book_by_author(author)
                if books:
                    print(Fore.GREEN + Style.BRIGHT + f"Books by {author_name}:")
                    for book in books:
                        print(Fore.GREEN + Style.BRIGHT + str(book))
                else:
                    print(Fore.RED + Style.BRIGHT + f"No books found for author '{author_name}'.")
                
            case '5':
                library.display_all_books()
                
            case '6':
                old_title = input(Fore.CYAN +"Enter old book title: ").strip().lower()
                new_title = input(Fore.CYAN +"Enter new book title: ").strip().lower()
                new_author_name = input(Fore.CYAN +"Enter new author name: ").strip().lower()
                new_description = input(Fore.CYAN +"Enter new description: ").strip().lower()
                new_page = input(Fore.CYAN +"Enter new page (optional): ").strip()
                new_page = int(new_page) if new_page else None
                library.edit_book(old_title, new_title, new_author_name, new_description, new_page)
                
            case '7':
                print(Fore.GREEN + Style.BRIGHT + "Logging out...")
                break
                
            case _:
                print(Fore.RED + Style.BRIGHT + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
