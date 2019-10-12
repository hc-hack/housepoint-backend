from models import AbstractModel
from argon2 import PasswordHasher
from uuid import uuid4
from argon2.exceptions import VerifyMismatchError

class account():
    def __init__(self, accountData):
        self.id = ""
        self.username = ""
        self.first_name= ""
        self.last_name= ""
        self.email = ""
        self.ability_rating = ""
        self.password = ""
        self.changes = {}

    def get_ID(self):
        return self.id
    def get_username(self):
        return self.username
    def get_first_name(self):
        return self.first_name
    def get_last_name(self):
        return self.last_name
    def get_email(self):
        return self.email
    def get_ability_rating(self):
        return self.ability_rating
    def get_password(self):
        return self.password

    def set_ID(self, accountData):             
                                
        if accountData[0] != None:
            self.changes["id"]=accountData[0]
    def set_username(self, accountData):
        if accountData[1] != None:
            self.changes["username"]=accountData[1]
    def set_first_name(self, accountData):
        if accountData[2] != None:
            self.changes["first_name"]=accountData[2]
    def set_last_name(self, accountData):
        if accountData[3] != None:
            self.changes["last_name"]=accountData[3]
    def set_email(self, accountData):
        if accountData[4] != None:
            self.changes["email"]=accountData[4]
    def set_ability_rating(self, accountData):
        if accountData[5] != None:
            self.changes["ability_rating"]=accountData[5]
    def set_password(self, accountData):
        if accountData[6] != None:
            self.changes["password"]=accountData[6]
    def commit(self):
        if (self.changes.get("id") != None):
            self.id = self.changes.get("id")
        if (self.changes.get("username") != None):
            self.username = self.changes.get("username")
        if (self.changes.get("first_name") != None):
            self.first_name = self.changes.get("first_name")
        if (self.changes.get("last_name") != None):     
            self.last_name = self.changes.get("last_name")
        if (self.changes.get("email") != None):
            self.email = self.changes.get("email")
        if (self.changes.get("ability_rating") != None): 
            self.ability_rating = self.changes.get("ability_rating")
        if (self.changes.get("password") != None):
            self.password = self.changes.get("password")


class AccountModel(AbstractModel):
    ACCOUNT_ZIP = ["id", "username", "first_name",
                   "last_name", "email", "ability_rating", "password"]

    def __init__(self):
        super().__init__()

    def _ensure_tables(self):
        """
        Ensure that the tables exist within the SQLite database
        """

        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                ability_rating INT,
                password TEXT
            )
        """)
        cursor.close()
        self.db.commit()

    def find_user(self, username=None, email=None, exclusive=False):
        """
        Locate a user using either a username or email
        """
        cursor = self.db.cursor()
        if username and email:
            if exclusive:
                cursor.execute(
                    """SELECT * FROM users WHERE username=? AND email=?""", (username, email,))
            else:
                cursor.execute(
                    """SELECT * FROM USERS WHERE username=? OR email=?""", (
                        username, email,)
                )  # TODO: What if there's two users?
        elif username:
            cursor.execute(
                """SELECT * FROM users WHERE username=?""", (
                    username,)
            )
        elif email:
            cursor.execute(
                """SELECT * FROM users WHERE email=?""", (email,))

        results = cursor.fetchall()

        if len(results) == 0:
            return None
        elif len(results) > 1:
            raise Exception("This shouldn't happen!")
        else:
            return results[0]

    def add_user(self, user):
        """ Insert the new user into the database """
        user_id = uuid4().hex
        first_name = user.get("first_name")
        last_name = user.get("last_name")
        username = user.get("username").lower()
        email = user.get("email")

        ph = PasswordHasher()
        password = ph.hash(user.get("password"))

        cursor = self.db.cursor()
        cursor.execute("""INSERT INTO users (id, username, first_name, last_name, email, ability_rating, password) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (user_id, username, first_name, last_name, email, -1, password))
        self.db.commit()
        ret_val = (True, user_id) if cursor.rowcount == 1 else (False, None)
        return ret_val

    def find_by_id(self, user_id):
        """ Looks up a user in the database by ID """
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        record = cursor.fetchone()
        return None if not record else dict(zip(self.ACCOUNT_ZIP, record))

    def delete_by_id(self, account_id):
        """
        Delete a user account by ID
        """
        account = self.find_by_id(account_id)
        if not account:
            return False, None
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (account_id,))

        success = cursor.rowcount == 1
        self.db.commit()

        return success, account

    def authenticate(self, username, password):
        """
        Returns the success and account, otherwise False and None
        """
        account = self.find_user(
            username=username, email=username, exclusive=False)
        if not account:
            return False, None
        account = dict(zip(self.ACCOUNT_ZIP, account))

        ph = PasswordHasher()
        try:
            valid = ph.verify(account.get("password"), password)
            if not valid:
                return False, account
            return True, account
        except VerifyMismatchError:
            return False, account
        finally:
            return False, None
