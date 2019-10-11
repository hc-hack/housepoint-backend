import sqlite3


class AccountModel():
    def __init__(self):
        self.db = sqlite3.connect('accounts/db.db')
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, firstname TEXT, secondname TEXT, 
            abilityrating INT, password TEXT)
        ''')
        self.db.commit()

    def createAccount(self, username: str, Firstname: str, Lastname: str, password: str, abilityRating: int):
        cursor = self.db.cursor()
        cursor.execute('''INSERT INTO users(username, firstname, secondname, abilityrating, password)
                          VALUES(?,?,?,?)''', (username, Firstname, Lastname, abilityRating, password))

    def getAccount(self, name: int, password: int):
        cursor = self.db.cursor()
        cursor.execute('''SELECT ALL FROM users WHERE username=? AND password=?''', (name, password,))
        return cursor.fetchone()

    def deleteAccount(self, id: int):
        cursor = self.db.cursor()
        cursor.execute('''DELETE ALL FROM users WHERE id=?''', id)
