import random
import sqlite3


conn = sqlite3.connect('card.s3db')


def luhn():
    bank_id = '400000'
    user_id = ''
    for num in range(9):
        user_id += str(random.randint(0, 9))
    card_num = bank_id + user_id
    lst = []
    for i in range(len(card_num)):
        if i % 2 == 0:
            num = int(card_num[i]) * 2
            if num >= 10:
                num -= 9
                lst.append(num)
            else:
                lst.append(num)
        else:
            num = int(card_num[i])
            lst.append(num)
    checksum = 10 - sum(lst) % 10
    if checksum == 10:
        checksum = 0
    card_num += str(checksum)
    return card_num


def check_luhn(transfer_card_number):
    lst = []
    for i in range(len(transfer_card_number) - 1):
        if i % 2 == 0:
            num = int(transfer_card_number[i]) * 2
            if num >= 10:
                num -= 9
                lst.append(num)
            else:
                lst.append(num)
        else:
            num = int(transfer_card_number[i])
            lst.append(num)
    checksum = 10 - sum(lst) % 10
    if checksum == 10:
        checksum = 0
    return checksum == int(transfer_card_number) % 10


def check_card(transfer_card_number):
    cur = conn.cursor()
    cur.execute('SELECT * FROM card WHERE number = ?;', (transfer_card_number,))
    res = cur.fetchone()
    conn.commit()
    if res == None:
        return 0
    return len(res)


def main_menu():
    print('1. Create an account\n2. Log into account\n0. Exit')
    n = int(input())
    if n == 1:
        create_account()
    elif n == 2:
        login_page()
    elif n == 0:
        print('Bye!')
        exit()


def login_page():
    card_input = str(input('Enter your card number: '))
    pin_input = str(input('Enter your PIN: '))
    cur = conn.cursor()
    cur.execute('SELECT * FROM card WHERE number = ?;', (card_input,))
    res = cur.fetchone()
    conn.commit()
    if res is not None and res[1] == card_input and res[2] == pin_input:
        print('You have successfully logged in!')
        personal_page(res[1])
    else:
        print('Wrong card number or PIN!')
        main_menu()


def personal_page(card_number):
    print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
    n = int(input())
    if n == 1:
        cur = conn.cursor()
        res = cur.execute('SELECT * FROM card WHERE number = ?', (card_number,)).fetchone()
        conn.commit()
        print('Balance: {}'.format(res[3]))
        personal_page(card_number)
    elif n == 2:
        income = int(input('Enter income: '))
        cur = conn.cursor()
        cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (income, card_number))
        conn.commit()
        print('Income was added!')
        personal_page(card_number)
    elif n == 3:
        transfer_card_number = str(input('Enter card number: '))
        if check_luhn(transfer_card_number) is not True:
            print('Probably you made a mistake in the card number. Please try again!')
            personal_page(card_number)
        elif check_card(transfer_card_number) == 0:
            print('Such a card does not exist.')
            personal_page(card_number)
        elif transfer_card_number == card_number:
            print("You can't transfer money to the same account!")
            personal_page(card_number)
        elif check_luhn(transfer_card_number) is True and check_card(transfer_card_number) > 0:
            amount = int(input('Enter how much money you want to transfer: '))
            cur = conn.cursor()
            cur.execute('SELECT * FROM card WHERE number = ?;', (card_number,))
            res = cur.fetchone()
            conn.commit()
            if res[-1] >= amount:
                cur = conn.cursor()
                cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (amount, transfer_card_number))
                cur.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (amount, card_number))
                conn.commit()
                print('Success!')
                personal_page(card_number)
            else:
                print('Not enough money!')
                personal_page(card_number)
    elif n == 4:
        cur = conn.cursor()
        cur.execute('DELETE FROM card WHERE number = ?', (card_number,))
        conn.commit()
        print('The account has been closed!')
        main_menu()
    elif n == 5:
        print('You have successfully logged out!')
        main_menu()
    elif n == 0:
        exit()


def create_account():
    pin = ''
    for num in range(4):
        pin += str(random.randint(0, 9))
    card_number = luhn()
    print('Your card has been created')
    print('Your card number:\n{}'.format(card_number))
    print('Your card PIN:\n{}'.format(pin))
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY, 
        number TEXT, 
        pin TEXT, 
        balance INTEGER DEFAULT 0);
        ''')
    cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (card_number, pin))
    conn.commit()
    main_menu()


if __name__ == '__main__':
    main_menu()
