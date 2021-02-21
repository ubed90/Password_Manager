import random , string
import os

def clear():
    return os.system('cls')

def random_password_generator_menu():
    clear()
    print('-'*30 + 'Menu' + '-'*30)
    print('1. Password(Only Uppercase & Lowercase)\n2. Password(Including Uppercase , Lowercase & digits)\n3. Password(Including Uppercase , Lowercase , digits & special characters)')
    print('-'*60)
    return input(':: ')

def generate_random_password():
    choice = random_password_generator_menu()
    if choice == '1':
        clear()
        k = input('Enter the length for your password :: ')
        # passwd = random.sample(list(string.ascii_letters) , k = int(k))
        return "".join(random.sample(list(string.ascii_letters) , k = int(k)))
    
    elif choice == '2':
        clear()
        k = input('Enter the length for your password :: ')
        # passwd = random.sample(list(string.ascii_letters + string.digits) , k = int(k))
        return "".join(random.sample(list(string.ascii_letters + string.digits) , k = int(k)))

    elif choice == '3':
        clear()
        k = input('Enter the length for your password :: ')
        # passwd = random.sample(list(string.ascii_letters + string.digits + '!@#$&*|_~') , k = int(k))
        return "".join(random.sample(list(string.ascii_letters + string.digits + '!@#$&*|_~') , k = int(k)))