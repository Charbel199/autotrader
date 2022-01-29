class UserAlreadyExistsException(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return f"User with email {self.email} already exists"
