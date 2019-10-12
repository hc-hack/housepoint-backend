from models import AbstractModel
from argon2 import PasswordHasher
from uuid import uuid4
from psycopg2 import sql
from argon2.exceptions import VerifyMismatchError


class Account():
    ACCOUNT_ZIP = ("id", "username", "first_name",
                   "last_name", "email", "ability_rating", "password")

    def __init__(self, account_data):
        self._changes = {}
        self._initialise(account_data)

    def __repr__(self):
        return '<Account username="{}">'.format(self._get_attribute("username"))

    def _initialise(self, account_data):
        """
        Loads the data into the object
        """
        self._original = dict(zip(self.ACCOUNT_ZIP, account_data))

    def _get_attribute(self, key):
        """ Gets the attribute if changed or original """
        if key in self._changes:
            return self._changes.get(key)
        return self._original.get(key)

    @property
    def dict(self):
        """ Returns the current account data as a dictionary """
        return {
            "id": self._get_attribute("id"),
            "username": self._get_attribute("username"),
            "email": self._get_attribute("email"),
            "first_name": self._get_attribute("first_name"),
            "last_name": self._get_attribute("last_name"),
            "ability_rating": self._get_attribute("ability_rating")
        }

    @property
    def id(self):
        return self._get_attribute("id")

    @property
    def username(self):
        return self._get_attribute("username")

    @property
    def first_name(self):
        return self._get_attribute("first_name")

    @property
    def last_name(self):
        return self._get_attribute("last_name")

    @property
    def email(self):
        return self._get_attribute("email")

    @property
    def ability_rating(self):
        return self._get_attribute("ability_rating")

    @property
    def password(self):
        return self._get_attribute("password")

    def _set_attribute(self, key, value):
        """ Persist changes into the changes dictionary """
        self._changes[key] = value

    @username.setter
    def username(self, value):
        self._set_attribute("username", value)

    @first_name.setter
    def first_name(self, value):
        self._set_attribute("first_name", value)

    @last_name.setter
    def last_name(self, value):
        self._set_attribute("last_name", value)

    @email.setter
    def email(self, value):
        self._set_attribute("email", value)

    @ability_rating.setter
    def ability_rating(self, value):
        self._set_attribute("ability_rating", value)

    @password.setter
    def password(self, value):
        self._set_attribute("password", value)

    # def commit(self):
    #     if (self.changes.get("id") != None):
    #         self.id = self.changes.get("id")
    #     if (self.changes.get("username") != None):
    #         self.username = self.changes.get("username")
    #     if (self.changes.get("first_name") != None):
    #         self.first_name = self.changes.get("first_name")
    #     if (self.changes.get("last_name") != None):
    #         self.last_name = self.changes.get("last_name")
    #     if (self.changes.get("email") != None):
    #         self.email = self.changes.get("email")
    #     if (self.changes.get("ability_rating") != None):
    #         self.ability_rating = self.changes.get("ability_rating")
    #     if (self.changes.get("password") != None):
    #         self.password = self.changes.get("password")


class AccountModel(AbstractModel):
    ACCOUNT_ZIP = ["id", "username", "first_name",
                   "last_name", "email", "ability_rating", "password"]

    def __init__(self):
        super().__init__()

    def _purge(self):
        """ This is a dev method - NEVER CALL THIS!!!! """
        cursor = self.conn.cursor()
        cursor.execute("DELETE from \"users\" WHERE 1=1")
        self.conn.commit()
        cursor.close()

    def _ensure_tables(self):
        """
        Ensure that the tables exist within the SQLite database
        """

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "users" (
	            "id" text,
	            "username" text,
	            "first_name" text,
	            "last_name" text,
	            "email" text,
	            "ability_rating" numeric(9,2),
	            "password" text,
	            PRIMARY KEY( id )
            );
        """)
        cursor.close()

    def find_user(self, username=None, email=None, exclusive=False):
        """
        Locate a user using either a username or email
        """
        cursor = self.conn.cursor()
        if username and email:

            if exclusive:
                cursor.execute(
                    sql.SQL("SELECT * FROM users WHERE username={} AND email={}").format(
                        sql.Literal(username),
                        sql.Literal(email)
                    ))
            else:
                cursor.execute(
                    sql.SQL("SELECT * FROM users WHERE username={} OR email={}").format(
                        sql.Literal(username),
                        sql.Literal(email)
                    )
                )  # TODO: What if there's more than one user?
        elif username:
            cursor.execute(
                sql.SQL("SELECT * FROM users WHERE username={}").format(
                    sql.Literal(username)
                )
            )
        elif email:
            cursor.execute(sql.SQL("SELECT * FROM users WHERE email={}").format(
                sql.Literal(email)
            ))

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

        cursor = self.conn.cursor()
        cursor.execute(
            sql.SQL("""
                INSERT INTO users (
                    id,
                    username,
                    first_name,
                    last_name,
                    email,
                    password)
                VALUES ({}, {}, {}, {}, {}, {})
                """).format(
                sql.Literal(user_id),
                sql.Literal(username),
                sql.Literal(first_name),
                sql.Literal(last_name),
                sql.Literal(email),
                sql.Literal(password)
            ))
        self.conn.commit()
        cursor.close()
        ret_val = (True, user_id) if cursor.rowcount == 1 else (False, None)
        return ret_val

    def find_by_id(self, user_id):
        """ Looks up a user in the database by ID """
        cursor = self.conn.cursor()
        cursor.execute(
            sql.SQL("SELECT * FROM users WHERE id={}").format(sql.Literal(user_id)))
        record = cursor.fetchone()
        return None if not record else self._objectify(record)

    def delete_by_id(self, account_id):
        """
        Delete a user account by ID
        """
        account = self.find_by_id(account_id)
        if not account:
            return False, None
        cursor = self.conn.cursor()
        cursor.execute(sql.SQL("DELETE FROM users WHERE id={}").format(
            sql.Literal(account_id)))

        success = cursor.rowcount == 1
        self.conn.commit()
        cursor.close()

        return success, account

    def authenticate(self, username, password):
        """
        Returns the success and account, otherwise False and None
        """
        account = self.find_user(
            username=username, email=username, exclusive=False)
        if not account:
            return False, None
        account = self._objectify(account)

        ph = PasswordHasher()
        try:
            valid = ph.verify(account.password, password)
            if not valid:
                return False, account
            return True, account

        except VerifyMismatchError:
            return False, account

        return False, None

    def _objectify(self, user):
        """ Transform the user data into the Account class """
        return Account(user)
