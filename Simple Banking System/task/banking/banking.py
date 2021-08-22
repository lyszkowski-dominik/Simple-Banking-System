from random import randint


credit_card_list = []


# Function responsible for displaying main menu
def main_menu():
    i = 0
    while i == 0:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        
        selection = input()
# Option number 1 - creating credit card and generating pin
        if selection == '1':
            print('Your card has been created')
            card = CreditCard()
            print('Your card number:')
            print(card.card_number)
            print('Your card PIN:')
            print(card.pin_number)
            credit_card_list.append(card)
# Option number 2 - logging into account
        elif selection == '2':
            login = input('Enter your card number: ')
            password = input('Enter your PIN: ')
            for n in credit_card_list:
                if int(n.get_card_number()) == int(login):
                    if int(n.get_pin_number()) == int(password):
                        print('You have successfully logged in!')
                        account_menu(n)
                        i = 1
                        break
            else:
                print('Wrong card number or PIN!')
# Option number 0 - exiting the main menu loop
        elif selection == '0':
            print('Bye!')
            i = 1
            break
# Option prompting choosing non existing option
        else:
            print("Unknown option selected")

# Function responsible for displaying menu after logging in


def account_menu(credit_card):
    while True:
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        selection = input()
        if selection == '1':
            print(credit_card.get_balance())
        elif selection == '2':
            print('You have successfully logged out!')
            main_menu()
            break
        elif selection == '0':
            print("Bye!")
            i = 1
            break


class CreditCard:
    
    def __init__(self):
        self.card_number = '400000' + str(randint(100000000, 999999999)) + str(randint(0, 9))
        self.pin_number = randint(1000, 9999)
        self.balance = 0

    def get_card_number(self):
        return self.card_number

    def get_pin_number(self):
        return self.pin_number

    def get_balance(self):
        return self.balance


# Starting the actual program
main_menu()
