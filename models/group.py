from models import AbstractModel
from psycopg2 import sql
from uuid import uuid4


class Group():
    GROUP_ZIP = ["id", "name", "users", "points"]

    def __init__(self, raw_group):
        self._original = dict(zip(self.GROUP_ZIP, raw_group))


class GroupModel(AbstractModel):
    GROUP_ZIP = ["id", "name", "private"]

    def _ensure_tables(self):
        """
        Ensure that the tables exists within PostgreSQL
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "groups" (
                "id" text,
                "name" text,
                "owner" text,
                "users" text[],
                "points" numeric(9,2),
                PRIMARY KEY( id )
            );
        """)
        cursor.close()

    def add_user_to_group(self, group_id, user_id):
        """ Adds a user ID to a group """
        group = self.get_group_by_id(group_id)

    def get_group_by_id(self, group_id):
        """ Fetches group by ID """
        cursor = self.conn.cursor()
        cursor.execute(sql.SQL("""
            SELECT * FROM "groups" WHERE id={}
        """).format(sql.Literal(group_id)))
        result = cursor.fetchone()
        if not result:
            return None
        return self._objectify(result)

    def new_group(self, group_name, creator):
        """
        Adds a new group with the first member being the current user
        """
        group_id = uuid4().hex
        cursor = self.conn.cursor()
        cursor.execute(sql.SQL("""
            INSERT INTO "groups" (id, name, owner, users, points) VALUES (?, ?, ?, ?, ?)
        """).format(
            sql.Literal(group_id),
            sql.Literal(group_name),
            sql.Literal(creator),
            sql.Literal([creator]),
            -1
        ))
        success = cursor.rowcount == 1
        cursor.close()
        return success, group_id

    @staticmethod
    def _objectify(result):
        return Group(result)
