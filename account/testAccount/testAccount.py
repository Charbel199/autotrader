from account.account import Account


class TestAccount(Account):

    def __init__(self):
        super().__init__()

    def get_position(self):
        return self.position

    def buy(self, symbol, amount, price):
        print("Bought ", amount, " of: ", symbol, " at ", price)
        print("New position ", self.position)

    def sold(self, symbol, amount, price):
        print("Sold ", amount, " of: ", symbol, " at ", price)
        print("New position ", self.position)

    @staticmethod
    def condition(name):
        return name == "testAccount"
