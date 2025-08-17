from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

