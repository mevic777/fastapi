def add(a: int, b: int):
    return a + b


class InsuficientFunds(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def widthdraw(self, amount):
        if amount > self.balance:
            raise InsuficientFunds("Insuficient funds")

        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
