def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


def showmenu():
    print("Choose an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
if __name__ == "__main__":
    while True:
        showmenu()
        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting...")
            break
        
        try:
            num1=float(input("Number one: "))
            num2=float(input("Number one: "))
        except ValueError:
            print("Please enter valid numbers.")
            continue
        
        match choice:
            case '1':
                print(f"{num1} + {num2} = {add(num1,num2)}")
            case '2':
                print(f"{num1} - {num2} = {subtract(num1,num2)}")
            case '3':
                print(f"{num1} * {num2} = {multiply(num1,num2)}")
            case '4':
                print(f"{num1} / {num2} = {divide(num1,num2)}")
            case _:
                print("Invalid choice, please try again.")
                
                             
