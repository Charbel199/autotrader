from abc import ABC, abstractmethod


class Account(ABC):

    def __init__(self):
        pass



    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get strategy
def get_account(name):
    for account in Account.__subclasses__():
        if account.condition(name):
            return account()
    return None
