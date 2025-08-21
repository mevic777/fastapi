import pytest
from app.calculations import add, BankAccount, InsuficientFunds

'''
    In order to run all the tests, we need to create a package test (with __init__.py)
    and after just run the command "pytest", and also there is a convention to write the python files for tests
    it it test_<name_of_file_where_is_the_function>.py, and also for the functions, 
    and also we need to name them test_<name_of_function_we_want_to_test>()

    pytest -v -> for extra verbosity(details of the test)
    pytest -s -> it will show all the print statements of the test
'''

# we are creating fixture that we could use in our test, check below
# def test_set_initial_bank_account(bank_account): or
# def test_bank_default_amount(zero_bank_account):


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (5, 3, 8),
    (3, 2, 5),
    (7, 5, 12)
])
def test_add(num1, num2, expected):
    print("testing add function")
    # assert True -> ~ to raising an error, when it is True -> nothing will happen, if false it will raise an error
    '''
        This is a feature of pytest that helps us to test our functions
        with different values and we have an example below.
    '''
    sum = add(num1, num2)
    assert sum == expected


def test_set_initial_bank_account(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_widthdraw(bank_account):
    bank_account.widthdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_collect(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, widhdrew, expected", [
    (200, 100, 100),
    (50, 25, 25),
    (10, 7, 3)
])
def test_bank_transaction(zero_bank_account, deposited, widhdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.widthdraw(widhdrew)

    assert zero_bank_account.balance == expected


def test_insuficient_funds(bank_account):
    with pytest.raises(InsuficientFunds):
        bank_account.widthdraw(200)
