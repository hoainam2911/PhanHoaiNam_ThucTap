# user.py
import json
from colorama import Fore

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password  

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password  
        }

    @staticmethod
    def from_dict(data):
        return User(data["username"], data["password"])

class UserManager:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.users = []
        self.load_users()

    def register(self, username, password):
        if self.find_user(username):
            print(Fore.RED + "❌ Tên người dùng đã tồn tại.")
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        print(Fore.GREEN + "✔ Đăng ký thành công.")
        return True

    def login(self, username, password):
        user = self.find_user(username)
        if user and user.password == password:
            print(Fore.GREEN + "✔ Đăng nhập thành công.")
            return True
        print(Fore.RED + "❌ Đăng nhập thất bại.")
        return False

    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def save_users(self):
        with open(self.filename, 'w') as file:
            data = [user.to_dict() for user in self.users]
            json.dump(data, file, indent=4)

    def load_users(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.users = [User.from_dict(item) for item in data]
                print(Fore.GREEN + "✔ Dữ liệu người dùng đã được tải.")
        except FileNotFoundError:
            print(Fore.YELLOW + "⚠ Không tìm thấy tệp người dùng. Bắt đầu với danh sách trống.")
            self.users = []
        except json.JSONDecodeError:
            print(Fore.RED + "❌ Dữ liệu người dùng không hợp lệ.")
            self.users = []
