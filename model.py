from app import *
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# Base de données fictive pour les utilisateurs
users = [
    User(1, "admin", "password1"),
    User(2, "user2", "password2"),
]
