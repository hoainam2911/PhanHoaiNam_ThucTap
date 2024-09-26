import json
from datetime import datetime
from colorama import init, Fore, Style
from user import UserManager

init(autoreset=True)

class Book:
    def __init__(self, title, author, book_id=None, date_added=None, pages=None):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.date_added = date_added or datetime.now().strftime("%Y-%m-%d")
        self.pages = pages

    def __str__(self):
        return f"'{self.title}' by {self.author.name} (ID: {self.book_id}, Added on: {self.date_added}, Pages: {self.pages})"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author.name,
            "id": self.book_id,
            "date_added": self.date_added,
            "pages": self.pages
        }

    @staticmethod
    def from_dict(data):
        author = Author(data["author"])
        return Book(
            title=data["title"],
            author=author,
            book_id=data.get("id"),
            date_added=data.get("date_added"),
            pages=data.get("pages")
        )

class Author:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Library:
    def __init__(self):
        self.books = []
        self.filename = "library_data.json"
        self.load_from_file()

    def add_book(self, book):
        book.title = book.title.strip()
        book.author.name = book.author.name.strip()
        book.book_id = len(self.books) + 1  # Assign an ID based on the current number of books
        self.books.append(book)
        print(Fore.GREEN + f"✔ Added: {book}")
        self.save_to_file()

    def remove_book(self, title):
        title = title.strip()
        for book in self.books:
            if book.title == title:
                confirm = input(Fore.YELLOW + f"Are you sure you want to delete the book '{title}'? (y/n): ")
                if confirm.lower() == 'y':
                    self.books.remove(book)
                    print(Fore.RED + f"❌ Deleted: {book}")
                    self.save_to_file()
                else:
                    print(Fore.CYAN + "Book deletion has been canceled.")
                return
        print(Fore.RED + f"Book with title '{title}' not found.")

    def find_book_by_title(self, title):
        title = title.strip()
        for book in self.books:
            if book.title == title:
                return book
        return None

    def find_book_by_author(self, author):
        author.name = author.name.strip()
        found_books = [book for book in self.books if book.author.name == author.name]
        return found_books

    def display_all_books(self):
        if not self.books:
            print(Fore.RED + "❌ No books in the library.")
        else:
            print(Fore.CYAN + "📚 List of books in the library:")
            print(Fore.CYAN + "-" * 90)
            print(Fore.LIGHTGREEN_EX + f"{'No.':<5}{'Title':<30}{'Author':<30}{'ID':<10}{'Date Added':<15}{'Pages':<6}")
            print(Fore.CYAN + "-" * 90)
            for idx, book in enumerate(self.books, 1):
                print(Fore.LIGHTYELLOW_EX + f"{idx:<5}{book.title:<30}{book.author.name:<30}{book.book_id:<10}{book.date_added:<15}{book.pages:<6}")
            print(Fore.CYAN + "-" * 90)

    def edit_book(self, old_title, new_title, new_author_name, new_pages=None):
        old_title = old_title.strip()
        new_title = new_title.strip()
        new_author_name = new_author_name.strip()
        book = self.find_book_by_title(old_title)
        if book:
            book.title = new_title
            book.author = Author(new_author_name)
            book.pages = new_pages
            print(Fore.GREEN + f"✔ Updated book: {book}")
            self.save_to_file()
        else:
            print(Fore.RED + f"❌ Book with title '{old_title}' not found.")

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            data = [book.to_dict() for book in self.books]
            json.dump(data, file, indent=4)
        print(Fore.GREEN + f"✔ Library data has been saved to {self.filename}.")

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                if file.read(1):
                    file.seek(0)
                    data = json.load(file)
                    self.books = [Book.from_dict(item) for item in data]
                    print(Fore.GREEN + f"✔ Library data has been loaded from {self.filename}.")
                else:
                    print(Fore.CYAN + f"File {self.filename} is empty. Library starts empty.")
                    self.books = []
        except FileNotFoundError:
            print(Fore.YELLOW + f"⚠ File {self.filename} not found. Library starts empty.")
            self.books = []
        except json.JSONDecodeError:
            print(Fore.RED + f"❌ File {self.filename} is not valid JSON. Library starts empty.")
            self.books = []

def main():
    library = Library()
    user_manager = UserManager()  # Initialize UserManager

    while True:
        print("\n" + Fore.LIGHTCYAN_EX + Style.BRIGHT + "=" * 40)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "📚 Library Management System".center(40))
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "=" * 40)

        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "1. Login")
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "2. Register")
        print(Fore.RED + "3. Exit")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "=" * 40)

        choice = input(Fore.YELLOW + Style.BRIGHT + "Enter your choice: ")

        match choice:
            case '1':
                username = input(Fore.LIGHTBLUE_EX + "Enter username: ")
                password = input(Fore.LIGHTBLUE_EX + "Enter password: ")
                if user_manager.login(username, password):
                    break
            
            case '2':
                username = input(Fore.LIGHTBLUE_EX + "Enter new username: ")
                password = input(Fore.LIGHTBLUE_EX + "Enter new password: ")
                user_manager.register(username, password)
            
            case '3':
                print(Fore.CYAN + "👋 Exiting...")
                return

            case _:
                print(Fore.RED + Style.BRIGHT + "❌ Invalid choice. Please enter a number between 1 and 3.")

    # After successful login, allow user to access library functions
    while True:
        print("\n" + Fore.LIGHTCYAN_EX + Style.BRIGHT + "=" * 40)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "📚 Library Management".center(40))
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "=" * 40)
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "1. Add book")
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "2. Remove book")
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "3. Find book by title")
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "4. List books by author")
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "5. Display all books")
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "6. Edit book")
        print(Fore.RED + "7. Logout")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "=" * 40)

        choice = input(Fore.YELLOW + Style.BRIGHT + "Enter your choice: ")

        match choice:
            case '1':
                title = input(Fore.LIGHTBLUE_EX + "Enter book title: ")
                author_name = input(Fore.LIGHTBLUE_EX + "Enter author name: ")
                pages = input(Fore.LIGHTBLUE_EX + "Enter number of pages: ")
                author = Author(author_name)
                try:
                    pages = int(pages)
                except ValueError:
                    pages = None
                    print(Fore.RED + "Invalid number of pages. Setting to None.")
                book = Book(title, author, pages=pages)
                library.add_book(book)
            
            case '2':
                title = input(Fore.LIGHTBLUE_EX + "Enter book title to delete: ")
                library.remove_book(title)
            
            case '3':
                title = input(Fore.LIGHTBLUE_EX + "Enter book title to find: ")
                book = library.find_book_by_title(title)
                if book:
                    print(Fore.GREEN + Style.BRIGHT + f"✔ Found: {book}")
                else:
                    print(Fore.RED + Style.BRIGHT + "❌ Book not found.")
            
            case '4':
                author_name = input(Fore.LIGHTBLUE_EX + "Enter author name to list books: ")
                author = Author(author_name)
                found_books = library.find_book_by_author(author)
                if found_books:
                    print(Fore.CYAN + f"📚 Found {len(found_books)} books by {author.name}:")
                    for book in found_books:
                        print(Fore.LIGHTYELLOW_EX + f"- {book}")
                else:
                    print(Fore.RED + Style.BRIGHT + f"❌ No books found by {author.name}.")
            
            case '5':
                library.display_all_books()

            case '6':
                old_title = input(Fore.LIGHTBLUE_EX + "Enter current book title to edit: ")
                new_title = input(Fore.LIGHTBLUE_EX + "Enter new title: ")
                new_author_name = input(Fore.LIGHTBLUE_EX + "Enter new author name: ")
                new_pages = input(Fore.LIGHTBLUE_EX + "Enter new number of pages: ")
                try:
                    new_pages = int(new_pages)
                except ValueError:
                    new_pages = None
                    print(Fore.RED + "Invalid number of pages. Setting to None.")
                library.edit_book(old_title, new_title, new_author_name, new_pages)
            
            case '7':
                print(Fore.CYAN + "👋 Logging out...")
                return

            case _:
                print(Fore.RED + Style.BRIGHT + "❌ Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
