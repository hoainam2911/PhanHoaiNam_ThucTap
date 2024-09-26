#user.py
import json
import uuid

class User:
    def __init__(self,username,password,user_id=None):
        self.username = username
        self.password = password
        self.user_id = user_id or str(uuid.uuid4())
        
    def to_dict(self):
        return {
            "id": self.user_id,
            "username": self.username,
            "password": self.password
        }
    
    @staticmethod
    def from_dict(d):
        return User(d["username"], d["password"], d["id"])
    
class UserManager:
    def __init__(self, filename='user.json'):
        self.filename = filename
        self.users = []
        self.load_user()
        
    def register(self, username, password):
        if self.find_user(username):
            print ("Usernames that already exist")
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        print("Registration is successful.")
        return True
    
    def login(self,username,password):
        user = self.find_user(username)
        if user and user.password == password:
            print("Login successful")
            return True
        print("Login failed")
        return False
    
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def save_users(self):
        with open(self.filename, 'w') as f:
            d = [user.to_dict() for user in self.users]
            json.dump(d, f, indent=4)
            
    def load_user(self):
        try:
            with open(self.filename, 'r') as f:
                d =json.load(f)
                self.users = [User.from_dict(item) for item in d]
                print("User data has been loaded.")
        except FileNotFoundError:
            print("User file not found. Start with an empty list.")
            self.users = []
        except json.JSONDecodeError:
            print("Invalid user data.")
            self.users = []
            