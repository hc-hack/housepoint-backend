import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import lookup
from psycopg2.errorcodes import DUPLICATE_DATABASE
from psycopg2 import sql


class AbstractModel():
    """
    Abstract model that handles the "nasties" of Postgres connections
    """
    USER = "postgres"
    PASSWORD = "password"
    HOST = "localhost"
    PORT = 5432
    DB_NAME = "hackathon_dev2"

    def __init__(self):
        self._make_database()
        self.conn = psycopg2.connect(user=self.USER, password=self.PASSWORD,
                                     host=self.HOST, port=self.PORT, dbname=self.DB_NAME)
        self._ensure_tables()

    def _ensure_tables(self):
        raise NotImplementedError()

    def _make_database(self):
        """
        Makes the database within postgres
        """
        # Throwaway connection
        conn = psycopg2.connect(user=self.USER, password=self.PASSWORD,
                                host=self.HOST, port=self.PORT, dbname="postgres")
        # Set autocommit isolation
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        try:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(self.DB_NAME), sql.Identifier(self.DB_NAME)))
        except lookup(DUPLICATE_DATABASE):
            # Allow a duplicate error!
            pass
        finally:
            conn.close()


if __name__ == "__main__":
    AbstractModel()
