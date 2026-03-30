def add(a: float, b: float) -> float:
    return a+b

def subtract(a: float, b: float) -> float:
    return a-b

class InsufficentFunds(Exception):
    pass

class BankAccount:
    """Простой класс банковского счёта"""
    
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    
    def deposit(self, amount):
        """Пополнение счёта"""
        self.balance += amount
    
    def withdraw(self, amount):
        """Снятие денег со счёта"""
        if amount >= self.balance:
            raise InsufficentFunds("Insufficient funds in account")

        self.balance -= amount
    
    def collect_interest(self):
        """Начисление 10% процентов (умножение баланса на 1.1)"""
        self.balance *= 1.1
