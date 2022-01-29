from .user_exception import UserException


class NotFoundException(UserException):
    def __str__(self):
        return "Not found"
