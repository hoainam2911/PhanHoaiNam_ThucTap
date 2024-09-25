import httpx # type: ignore
from tabulate import tabulate # type: ignore

def fetch_all_todos():
    url = "https://jsonplaceholder.typicode.com/todos"
    response = httpx.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Lỗi {response.status_code}")
        return []

def print_todos_table(todos):
    table = []
    headers = ["ID", "Title", "Completed"]
    
    for todo in todos:
        table.append([todo['id'], todo['title'], "Yes" if todo['completed'] else "No"])
    
    print(tabulate(table, headers, tablefmt="grid"))

if __name__ == "__main__":
    todos = fetch_all_todos()
    if todos:
        print_todos_table(todos)
