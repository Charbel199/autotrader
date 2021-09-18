from account.account import Account


class TestAccount(Account):

    def __init__(self):
        super().__init__()

    @staticmethod
    def condition(name):
        return name == "testAccount"
