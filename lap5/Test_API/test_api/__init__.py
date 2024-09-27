import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

API_URL = "http://127.0.0.1:5000/books"

def print_message(message, color=Fore.GREEN):
    print(color + message + Style.RESET_ALL)

def validate_book_input(title, author, published_year):
    errors = []
    if not isinstance(title, str) or not title:
        errors.append("Title must be a non-empty string.")
    if not isinstance(author, str) or not author:
        errors.append("Author must be a non-empty string.")
    if not isinstance(published_year, int) or published_year < 1000 or published_year > 9999:
        errors.append("Published year must be an integer between 1000 and 9999.")
    return errors

def add_book():
    print_message("\n--- Add New Book ---", Fore.CYAN)
    while True:
        title = input("Enter the book title: ")
        author = input("Enter the author's name: ")
        try:
            published_year = int(input("Enter the publication year: "))
        except ValueError:
            print_message("Published year must be an integer.", Fore.RED)
            continue

        errors = validate_book_input(title, author, published_year)
        if errors:
            print_message("Errors: " + ", ".join(errors), Fore.RED)
            continue
        
        data = {
            "title": title,
            "author": author,
            "published_year": published_year
        }
        
        response = requests.post(API_URL, json=data)
        print_message(response.json().get('message', 'Error occurred'), Fore.GREEN)
        break

def view_books():
    print_message("\n--- View All Books ---", Fore.CYAN)
    response = requests.get(API_URL)
    books = response.json()
    
    if not books:
        print_message("No books available.", Fore.YELLOW)
    else:
        print_message(f" {'ID':<10} {'Title':<30} {'Author':<30} {'Year':<30}", Fore.MAGENTA + Style.BRIGHT)
        for book in books:
            print_message(f" {book['id']:<10} {book['title']:<30} {book['author']:<30} {book['published_year']:<30}", Fore.GREEN)

def update_book():
    print_message("\n--- Update Book Information ---", Fore.CYAN)
    while True:
        try:
            book_id = int(input("Enter the ID of the book to update: "))
        except ValueError:
            print_message("ID must be an integer.", Fore.RED)
            continue

        title = input("Enter the new title of the book (or leave blank to keep current): ")
        author = input("Enter the new author's name (or leave blank to keep current): ")
        try:
            published_year = input("Enter the new publication year (or leave blank to keep current): ")
            if published_year:
                published_year = int(published_year)
            else:
                published_year = None
        except ValueError:
            print_message("Published year must be an integer.", Fore.RED)
            continue

        data = {}
        if title:
            data['title'] = title
        if author:
            data['author'] = author
        if published_year is not None:
            data['published_year'] = published_year

        response = requests.put(f"{API_URL}/{book_id}", json=data)
        print_message(response.json().get('message', 'Error occurred'), Fore.GREEN)
        break

def delete_book():
    print_message("\n--- Delete Book ---", Fore.CYAN)
    while True:
        try:
            book_id = int(input("Enter the ID of the book to delete: "))
        except ValueError:
            print_message("ID must be an integer.", Fore.RED)
            continue
        
        response = requests.delete(f"{API_URL}/{book_id}")
        print_message(response.json().get('message', 'Error occurred'), Fore.GREEN)
        break

def main():
    while True:
        print_message("\nLibrary Management System:", Fore.YELLOW)
        print("1. Add a book")
        print("2. View all books")
        print("3. Update a book")
        print("4. Delete a book")
        print("5. Exit", Fore.RED)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            update_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            print_message("Thank you for using the Library Management System. Goodbye!", Fore.MAGENTA)
            break
        else:
            print_message("Invalid choice, please try again.", Fore.RED)

if __name__ == "__main__":
    main()
