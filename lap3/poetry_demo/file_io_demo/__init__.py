def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def read_from_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found!"

if __name__ == "__main__":
    filename = "demo.txt"
    
    
    print("=== INPUT TEXT === ")
    content = input("Text: ")
    # Ghi nội dung vào tệp
    write_to_file(filename, content)
    
    # Đọc nội dung từ tệp
    print("Nội dung của tệp:")
    print(read_from_file(filename))
