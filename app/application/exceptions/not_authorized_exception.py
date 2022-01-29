class NotAuthorizedException(Exception):
    def __str__(self):
        return "User is not authorized"
