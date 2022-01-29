from .user_exception import UserException


class WrongPasswordException(UserException):
    def __str__(self):
        return "Wrong password"
