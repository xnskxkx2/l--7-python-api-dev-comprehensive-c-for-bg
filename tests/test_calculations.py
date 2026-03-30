import pytest

from app.calculations import BankAccount, InsufficentFunds, add, subtract


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("a, b, expected", [(4, 2, 6), (5, 8, 13), (3, 2, 5)])
def test_add(a, b, expected):
    print("\nStarting test add...")
    assert add(a, b) == expected


def test_subtract():
    difference = subtract(2, 3)
    assert difference == -1


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60


def test_bank_withdraw(bank_account):
    bank_account.withdraw(-10)
    assert bank_account.balance == 60


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize(
    "deposited, withdrew, expected", [(50, 20, 30), (20, 10, 10), (100, 0, 100)]
)
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficent_funds(bank_account):
    with pytest.raises(InsufficentFunds):
        bank_account.withdraw(100)
