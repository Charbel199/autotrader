class WrongPasswordException(Exception):
    def __str__(self):
        return "Wrong password"

