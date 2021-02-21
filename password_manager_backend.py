import mysql.connector as mc
import re

password = ''
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

#FUNCTION TO ASK PASSWORD FOR ROOT_USER (PRESS ENTER IF NO PASS)
def ask_for_master_password():
    global password
    password = input('Enter the MASTER PASSWORD to gain Access to the VAULT (IF NO PASS PRESS ENTER) :: ') or None
    try:
        conn = mc.connect(
        host = 'localhost',
        user = 'root',
        password = password 
    )
    except:
        return False
    conn.close()
    return True

# FUNCTON TO CREATE DATABASE
def create_db():
    conn = mc.connect(
        host = 'localhost',
        user = 'root',
        password = password,
    )
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS password_manager')
    conn.commit()
    conn.close()


# CLASS TO MAKE THE MANAGER WORK
class password_manager_backend:
    # password = ''
    global password
    def __init__(self):
        self.conn = mc.connect(
        host = 'localhost',
        user = 'root',
        password = password,
        database = 'password_manager'
    )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        try:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS Accounts (email VARCHAR(100) PRIMARY KEY, password VARCHAR(100) NOT NULL)')
            self.conn.commit()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS Apps (id INT AUTO_INCREMENT PRIMARY KEY , email_id VARCHAR(100), password VARCHAR(100) NOT NULL , username VARCHAR(100) DEFAULT NULL , phone VARCHAR(20) DEFAULT NULL , app_name VARCHAR(100) NOT NULL)')
            self.conn.commit()
        except mc.Error as error:
            print(error)

    def check_valid_email(self , email):
        if(re.search(regex,email)):
            return True
        else:
            return False  

    def check_email_registry(self , email):
        self.cursor.execute('SELECT email FROM Accounts')
        all_emails = self.cursor.fetchall()
        for emails in all_emails:
            if emails[0] == email:
                return True
        else:
            return False

    def insert_into_accounts(self , email , password):
        if self.check_valid_email(email):
            try:
                query = 'INSERT INTO Accounts (email , password) VALUES (%s , %s)'
                self.cursor.execute(query , (email , password))
                self.conn.commit()
                return True
            except mc.errors.IntegrityError:
                return False
        else:
            return False


    def insert_into_apps(self , email , password , app_name , username=None , phone=None):
        try:
            if self.check_email_registry(email) and self.check_valid_email(email):
                query = 'INSERT INTO Apps (email_id , password , username , phone , app_name) VALUES (%s , %s , IFNULL(%s , DEFAULT(username)) , IFNULL(%s , DEFAULT(phone)) , %s)'
                self.cursor.execute(query , (email , password , username , phone ,  app_name))
                self.conn.commit()
                return True
            else:
                return False
        except mc.Error as error:
            print(error)
    
    def update_account_password(self , email , password):
        if self.check_valid_email(email):
            try:
                self.cursor.execute('UPDATE Accounts SET password = %s WHERE email = %s' , (password , email))
                self.conn.commit()
            except:
                return False
            return True
        else:
            return False

    def update_app_credentials(self , id , email , password , username , phone , app_name):
        try:
            if self.check_email_registry(email=email) and self.check_valid_email(email=email):
                self.cursor.execute('UPDATE Apps SET email_id = %s , password = %s , username = %s , phone = %s , app_name = %s WHERE id = %s' , (email , password , username , phone , app_name , id))
                self.conn.commit()
                return True
            else:
                return False
        except mc.Error as error:
            print(error)

    def get_account_pass(self , email):
        try:
            if self.check_email_registry(email=email) and self.check_valid_email(email=email):
                self.cursor.execute('SELECT password FROM Accounts WHERE email = %s' , (email , ))
                data = self.cursor.fetchone()
                return data
            else:
                return False
        except mc.Error as error:
            print(error)

    def get_specific_accounts_apps_data(self , email=None , app_name = None , id = None):
        try:
            self.cursor.execute('SELECT * FROM Apps WHERE id = %s or email_id = %s or app_name = %s' , (id , email , app_name))
            data = self.cursor.fetchall()
            return data
        except mc.Error as error:
            print(error)


    def get_all_apps(self):
        try:
            self.cursor.execute('SELECT * FROM Apps')
            data = self.cursor.fetchall()
            return data
        except mc.Error as error:
            print(error)

    def get_all_accounts(self):
        try:
            self.cursor.execute('SELECT * FROM Accounts')
            data = self.cursor.fetchall()
            return data
        except mc.Error as error:
            print(error)

    def del_account_or_app(self , email = None , id = None):
        try:
            if email == None:
                self.cursor.execute('DELETE FROM Apps WHERE id = %s' , (id,))
                self.conn.commit()
            else:
                if self.check_email_registry(email) and self.check_valid_email(email):
                    self.cursor.execute('DELETE FROM Accounts WHERE email = %s' , (email,))
                    self.conn.commit()
                    return True
                else:
                    return False
        except mc.Error as error:
            print(error)

    def iexit(self):
        self.conn.close()
        exit()