import json
import os

# Tệp lưu trữ dữ liệu liên hệ
CONTACTS_FILE = 'danhba.json'

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Tệp JSON bị lỗi. Tạo một tệp mới.")
                return {}
    return {}

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

def create_contact(name, phone):
    contacts = load_contacts()
    contacts[name] = phone
    save_contacts(contacts)
    print(f"Liên hệ '{name}' đã được thêm vào danh bạ.")

def read_contacts():
    contacts = load_contacts()
    if not contacts:
        print("Danh bạ rỗng.")
    else:
        for name, phone in contacts.items():
            print(f"Tên: {name}, Điện thoại: {phone}")

def update_contact(name, new_phone):
    contacts = load_contacts()
    if name in contacts:
        contacts[name] = new_phone
        save_contacts(contacts)
        print(f"Thông tin liên hệ '{name}' đã được cập nhật.")
    else:
        print(f"Không tìm thấy liên hệ với tên '{name}'.")

def delete_contact(name):
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print(f"Liên hệ '{name}' đã được xóa khỏi danh bạ.")
    else:
        print(f"Không tìm thấy liên hệ với tên '{name}'.")




        
            
def main():
       while True:
        print("\nQuản lý danh bạ")
        print("1. Thêm liên hệ")
        print("2. Xem danh bạ")
        print("3. Cập nhật liên hệ")
        print("4. Xóa liên hệ")
        print("5. Thoát")

        choice =int(input("Chọn tùy chọn (1/2/3/4/5): "))
        match choice:
            case 1:
                name = input("Nhập tên liên hệ: ")
                phone = input("Nhập số điện thoại: ")
                create_contact(name, phone)
            case 2:
                read_contacts()
            case 3:
                name = input("Nhập tên liên hệ cần cập nhật: ")
                new_phone = input("Nhập số điện thoại mới: ")
                update_contact(name, new_phone)
            case 4:
                name = input("Nhập tên liên hệ cần xóa: ")
                delete_contact(name)
            case _:
                break
        
if __name__ == "__main__":
    main()
