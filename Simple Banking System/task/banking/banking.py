from random import randint
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


# Function responsible for displaying main menu


def main_menu():
    while True:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

        selection = input()
# Option number 1 - creating credit card and generating pin
        if selection == '1':
            print('Your card has been created')
            card = CreditCard()
            cur.execute("INSERT INTO card (number,pin) VALUES ('" + card.card_number + "', '" + card.pin_number + "')")
            conn.commit()
            print('Your card number:')
            print(card.card_number)
            print('Your card PIN:')
            print(card.pin_number)

# Option number 2 - logging into account
        elif selection == '2':
            login = input('Enter your card number: ')
            password = input('Enter your PIN: ')
            cur.execute("SELECT number FROM card WHERE number = " + login + "")
            entered_login = str(cur.fetchone())
            cur.execute("SELECT pin FROM card WHERE pin = " + password + "")
            entered_pin = str(cur.fetchone())
            entered_login = clean_sql_query(entered_login)
            entered_pin = clean_sql_query(entered_pin)
            if entered_login == login:
                if entered_pin == password:
                    print('You have successfully logged in!')
                    account_menu(entered_login)
                    break
                else:
                    print('Wrong card number or PIN!')
            else:
                print('Wrong card number or PIN!')
# Option number 0 - exiting the main menu loop
        elif selection == '0':
            print('Bye!')
            break
# Option prompting choosing non existing option
        else:
            print("Unknown option selected")


# Function responsible for displaying menu after logging in
def account_menu(account_number):
    while True:
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        selection = input()
        if selection == '1':
            cur.execute("SELECT balance FROM card WHERE number = " + account_number + "")
            balance = str(cur.fetchone())
            balance = clean_sql_query(balance)
            print(balance)
        elif selection == '2':
            income = int(input('Enter income:'))
            cur.execute("SELECT balance FROM card WHERE number = " + account_number + "")
            balance = str(cur.fetchone())
            balance = clean_sql_query(balance)
            balance = int(balance)
            balance += income
            balance = str(balance)
            cur.execute("UPDATE card SET balance = " + balance + " WHERE number = " + account_number + "")
            conn.commit()
            print('Income was added!')
        elif selection == '3':
            card_number = input('Enter card number:')
            if card_number_validator(card_number) == 1:
                do_transfer(card_number, account_number)

        elif selection == '4':
            cur.execute("DELETE from card WHERE number = " + account_number + "")
            conn.commit()
            print('The account has been closed!')
            main_menu()
            break
        elif selection == '5':
            print('You have successfully logged out!')
            main_menu()
            break
        elif selection == '0':
            print("Bye!")
            break


# Class responsible for creating credit cards
class CreditCard:

    def __init__(self):
        self.card_number = card_number_creator()
        self.pin_number = str(randint(1000, 9999))
        self.balance = 0


# method used to create valid credit card number while using Luhn algorithm
def card_number_creator():
    temporary_card_number = '400000' + str(randint(100000000, 999999999))
    card_number_list = []
    counter = 0
    for x in temporary_card_number:
        card_number_list.append(x)
    i = 0
    while i < len(card_number_list):
        if (i % 2) == 0:
            card_number_list[i] = int(card_number_list[i]) * 2
            if card_number_list[i] > 9:
                card_number_list[i] -= 9
        card_number_list[i] = int(card_number_list[i])
        i += 1
    sum_of_digits = sum(card_number_list)
    if sum_of_digits % 10 == 0:
        card_number = temporary_card_number + '0'
        return card_number
    else:
        modulo = sum_of_digits % 10
        while modulo % 10 != 0:
            modulo += 1
            counter += 1
    card_number = temporary_card_number + str(counter)
    return card_number


def card_number_validator(card_n):
    card_n_list = []
    for x in card_n:
        card_n_list.append(x)
    i = 0
    while i < len(card_n_list):
        if (i % 2) == 0:
            card_n_list[i] = int(card_n_list[i]) * 2
            if card_n_list[i] > 9:
                card_n_list[i] -= 9
        card_n_list[i] = int(card_n_list[i])
        i += 1
    sum_of_digits = sum(card_n_list)
    modulo = sum_of_digits % 10
    if modulo == 0:
        return 1
    else:
        print("Probably you made a mistake in the card number. Please try again!")
        return 0


def clean_sql_query(word):
    word = word.replace('(', '')
    word = word.replace("'", '')
    word = word.replace(",", '')
    word = word.replace(")", '')
    return word


def check_if_table_exists():
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='card'")
    result = str(cur.fetchone())
    result = clean_sql_query(result)
    result = int(result)
    if result == 1:
        print('Successfully connected to database')
    else:
        print('Database does not exist. Creating one')
        cur.execute('CREATE TABLE card (id INTEGER , number TEXT, pin TEXT, balance INTEGER DEFAULT 0 );')
        conn.commit()


def print_whole_table():
    cur.execute('SELECT  number AS number, pin AS pin, balance AS balance FROM card')
    print(cur.fetchall())


# have to implement Luhn algorithm to validate given card number
def do_transfer(card_number, account_number):
    cur.execute("SELECT number FROM card WHERE number = " + card_number + "")
    acc_number = str(cur.fetchone())
    acc_number = clean_sql_query(acc_number)
    if account_number == card_number:
        print("You can't transfer money to the same account!")
    elif acc_number == card_number:
        to_transfer = int(input('Enter how much money you want to transfer:'))
        cur.execute("SELECT balance FROM card WHERE number = " + account_number + "")
        my_balance = str(cur.fetchone())
        my_balance = clean_sql_query(my_balance)
        my_balance = int(my_balance)
        if my_balance > to_transfer:
            my_balance -= to_transfer
            my_balance = str(my_balance)
            cur.execute("UPDATE card SET balance = " + my_balance + " WHERE number = " + account_number + "")
            conn.commit()
            cur.execute("SELECT balance FROM card WHERE number = " + card_number + "")
            other_balance = str(cur.fetchone())
            other_balance = clean_sql_query(other_balance)
            other_balance = int(other_balance)
            other_balance += to_transfer
            other_balance = str(other_balance)
            cur.execute("UPDATE card SET balance = " + other_balance + " WHERE number = " + card_number + "")
            conn.commit()
            print('Success!')
        else:
            print('Not enough money!')
    else:
        print('Such a card does not exist')


# Starting the actual program
check_if_table_exists()
print_whole_table()
main_menu()
