import os
from typing import get_args
from random_password_generator import generate_random_password
from password_manager_backend import ask_for_master_password , create_db , password_manager_backend
import pyperclip
from prettytable import PrettyTable

flag = True

def clear():
    return os.system('cls')


def menu():
    print('-'*30 + 'Menu' + '-'*30)
    print('1. GENERATE Random Password.\n2. REGISTER a new Email_Id & Password\n3. ADD an App / Site Linked to an Registered\
 Email\n4. GET Apps / sites registered to an Email\n5. SEARCH for App / site to view registered accounts\n6. VIEW all registered Emails\n7. VIEW all\
 Registered Apps\n8. UPDATE EMAIL credentials from ACCOUNTS\n9. UPDATE App data / Credentials\n10. DELETE Account or App\n11. VIEW Passwords\n12. EXIT')
    print('-'*60)
    return input(':: ')


if ask_for_master_password():
        create_db()
        password_manager = password_manager_backend()
        password_manager.create_tables()
        clear()
        print('WElCOME MASTER !')
else:
        print('Invalid Password or Check MySql State...\nTry Again!!')
        flag = False


while flag:
    choice = menu()
    while choice not in ['1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '10' , '11' , '12']:
        clear()
        print('Invalid Choice...\nPlease enter between (1-10)')
        choice = menu()
    else:
        if choice == '1':
            password = generate_random_password()
            pyperclip.copy(password)
            pyperclip.paste()
            clear()
            print('GENERATED PASSWORD HAS BEEN COPIED TO YOUR CLIPBOARD !!')
            # flag = False

        elif choice == '2':
            clear()
            email = input('ENTER EMAIL :: ').lower()
            password = input('ENTER PASSWORD :: ')
            if password_manager.insert_into_accounts(email , password):
                clear()
                print(f'{email} REGISTERED SUCCESSFULLY !!')
            else:
                clear()
                print(f'{email} ALREADY REGISTERED or {email} NOT VALID !!')

        elif choice == '3':
            clear()
            email = input('ENTER EMAIL :: ').lower()
            password = input('ENTER PASSWORD :: ')
            username = input('ENTER USERNAME(press ENTER if NONE) :: ') or None
            phone = input('ENTER PHONE NO (press ENTER if NONE) :: ') or None
            app_name = input('ENTER App / Site Name :: ')
            if password_manager.insert_into_apps(email , password , app_name , username , phone):
                clear()
                print(f'APP "{app_name}" CREDENTIALS SAVED SUCCESSFULLY !')
            else:
                clear()
                print(f'{email} NOT REGISTERED (REGISTER IT IN ACCOUNTS SECTION FIRST) or {email} NOT VALID !!')

        elif choice == '4':
            clear()
            email = input('ENTER EMAIL :: ').lower()
            all_accs = password_manager.get_specific_accounts_apps_data(email = email)
            if len(all_accs) == 0:
                clear()
                print('NO RECORDS FOUND')
            else:
                clear()
                myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                for row in all_accs:
                    myTable.add_row(row[0:2]+row[3:])
                print(myTable)

        elif choice == '5':
            clear()
            app_name = input('ENTER App / Site Name :: ')
            all_accs = password_manager.get_specific_accounts_apps_data(app_name = app_name)
            if len(all_accs) == 0:
                clear()
                print('NO RECORDS FOUND')
            else:
                clear()
                myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                for row in all_accs:
                    myTable.add_row(row[0:2]+row[3:])
                print(myTable)
        
        elif choice == '6':
            all_accs = password_manager.get_all_accounts()
            if len(all_accs) == 0:
                clear()
                print('NO REGISTERED EMAILS')
            else:
                clear()
                myTable = PrettyTable(['EMAIL'])
                for row in all_accs:
                    myTable.add_row(row[0:1])
                print(myTable)

        elif choice == '7':
            all_accs = password_manager.get_all_apps()
            if len(all_accs) == 0:
                clear()
                print('NO REGISTERED APPS / SITES')
            else:
                clear()
                myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                for row in all_accs:
                    myTable.add_row(row[0:2]+row[3:])
                print(myTable)

        elif choice == '8':
            all_accs = password_manager.get_all_accounts()
            if len(all_accs) == 0:
                clear()
                print('NO REGISTERED EMAILS')
            else:
                clear()
                myTable = PrettyTable(['EMAIL'])
                for row in all_accs:
                    myTable.add_row(row[0:1])
                print(myTable)
                email = input('ENTER EMAIL (EXACT) YOU WISH TO CHNAGE THE PASSWORD :: ').lower()
                password = input('ENTER NEW PASSWORD :: ')
                if password_manager.update_account_password(email = email , password = password):
                    clear()
                    print(f'Password for {email} UPDATED SUCESSFULLY')
                else:
                    clear()
                    print('EMAIL NOT FOUND OR INVALID EMAIL')

        elif choice == '9':
            all_accs = password_manager.get_all_apps()
            if len(all_accs) == 0:
                clear()
                print('NO REGISTERED APPS / SITES')
            else:
                clear()
                myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                for row in all_accs:
                    myTable.add_row(row[0:2]+row[3:])
                print(myTable)
                id = input('ENTER CORRESPONDING "ID" of App / Site which you want to update Credentials :: ')
                data = password_manager.get_specific_accounts_apps_data(id = id)
                if len(data) == 0:
                    clear()
                    print('INVALID ID !!')
                else:
                    data = data[0]
                    clear()
                    myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                    myTable.add_row(data[0:2]+data[3:])
                    print(myTable)
                    print(f'ENTER Credentials to UPDATE for ID --> {id}\nIn Case You dont want to change something press ENTER without typing...')
                    email = input('ENTER EMAIL :: ') or data[1]
                    password = input('ENTER PASSWORD :: ') or data[2]
                    username = input('ENTER USERNAME :: ') or data[3]
                    phone = input('ENTER PHONE NO :: ') or data[4]
                    app_name = input('ENTER APP / SITE Name :: ') or data[5]
                    if password_manager.update_app_credentials(id = id , email = email , password = password , username = username , phone = phone , app_name = app_name):
                        clear()
                        print(f'CREDENTIALS for {app_name} updated Successfully !')
                    else:
                        clear()
                        print(f'{email} NOT REGISTERED (REGISTER IT IN ACCOUNTS SECTION FIRST) or {email} NOT VALID !!')

        elif choice == '10':
            clear()
            wtd = input('WHAT YOU WANT TO DELETE ?\n1. REGISTERED EMAIL\n2. REGISTERED APP / SITE\n:: ')
            if wtd not in ['1' , '2']:
                clear()
                print('Invalid Choice !')
            elif wtd == '1':
                clear()
                all_accs = password_manager.get_all_accounts()
                if len(all_accs) == 0:
                    clear()
                    print('NO REGISTERED EMAILS')
                else:
                    clear()
                    myTable = PrettyTable(['EMAIL'])
                    for row in all_accs:
                        myTable.add_row(row[0:1])
                    print(myTable)
                    email = input('ENTER EMAIL (EXACT) :: ').lower()
                    if password_manager.del_account_or_app(email = email):
                        clear()
                        print(f'{email} DELETED SUCCESSFULLY...!')
                    else:
                        clear()
                        print(f'{email} NOT FOUND or {email} NOT VALID')
            elif wtd == '2':
                clear()
                all_accs = password_manager.get_all_apps()
                if len(all_accs) == 0:
                    clear()
                    print('NO REGISTERED APPS / SITES')
                else:
                    clear()
                    myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                    for row in all_accs:
                        myTable.add_row(row[0:2]+row[3:])
                    print(myTable)
                    id = input('ENTER CORRESPONDING "ID" of App / Site which you want to DELETE :: ')
                    data = password_manager.get_specific_accounts_apps_data(id = id)
                    if len(data) == 0:
                        clear()
                        print('INVALID ID !!')
                    else:
                        data = data[0]
                        clear()
                        password_manager.del_account_or_app(id = id)
                        print(f'{data[5]} app with ID --> {id} DELETED SUCCESSFULLY..!')
        
        elif choice == '11':
            clear()
            wtd = input('FOR WHAT YOU WANT TO KNOW THE PASSWORD FOR ?\n1. REGISTERED EMAIL\n2. REGISTERED APP / SITE\n:: ')
            if wtd not in ['1' , '2']:
                clear()
                print('Invalid Choice !')
            elif wtd == '1':
                clear()
                all_accs = password_manager.get_all_accounts()
                if len(all_accs) == 0:
                    clear()
                    print('NO REGISTERED EMAILS')
                else:
                    clear()
                    myTable = PrettyTable(['EMAIL'])
                    for row in all_accs:
                        myTable.add_row(row[0:1])
                    print(myTable)
                    email = input('ENTER EMAIL (EXACT) :: ').lower()
                    get_acc_data = password_manager.get_account_pass(email = email)
                    if get_acc_data != False:
                        clear()
                        print(f'PASSWORD for the {email} is :: {get_acc_data[0]}')
                    else:
                        clear()
                        print(f'{email} NOT REGISTERED or {email} NOT VALID !')

            elif wtd == '2':
                clear()
                all_accs = password_manager.get_all_apps()
                if len(all_accs) == 0:
                    clear()
                    print('NO REGISTERED APPS / SITES')
                else:
                    clear()
                    myTable = PrettyTable(['ID' , 'EMAIL' , 'USERNAME' , 'PHONE' , 'APP / SITE'])
                    for row in all_accs:
                        myTable.add_row(row[0:2]+row[3:])
                    print(myTable)
                    id = input('ENTER CORRESPONDING "ID" of App / Site which you want to know the PASSWORD :: ')
                    data = password_manager.get_specific_accounts_apps_data(id = id)
                    if len(data) == 0:
                        clear()
                        print('INVALID ID !!')
                    else:
                        data = data[0]
                        clear()
                        print(f'The Password for account of {data[5]} linked to {data[1]} is :: {data[2]}')
            


        elif choice == '12':
            clear()
            print('UNTIL WE MEET AGAIN....')
            exit()

