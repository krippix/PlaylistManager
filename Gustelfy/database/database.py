# external
# python native
import logging
# project
#import util.config
from Gustelfy.database import interface, sqlite_con, oracle_con


class Database():
    '''Returns chosen class type. e.g SQLite or Postgres. Defaults to sqlite3'''

    connection: interface.Interface # Represents the chosen database connection

    # Constructor: Check if input type exists, defaults to sqlite3, returns db-connection
    def __init__(self, connection="sqlite3"):
        # define available databases, and assign their caller
        db_types = {
            "sqlite3": self.sqlite3,
            "oracledb": self.oracledb
        }
        logger.info("Establishing database connection.")
        if not connection in db_types:
            raise KeyError()
        else:
            self.connection = db_types[connection]()
            self.connection.check()

    # ---- Getter Functions ----

    def get_db_connection(self) -> interface.Interface:
        """Returns previously initialized database connection.

        Returns:
            interface.Interface: Chosen database connection
        """
        return self.connection

    # ---- Setter Functions ----
    
    # ---- Other Functions ----

    def sqlite3(self):
        """Creates sqlite3 database connection

        Returns:
            SqliteCon: SqliteCon
        """
        return sqlite_con.SqliteCon()

    def oracledb(self):
        """Creates oracle database connection

        Returns:
            OracleCon: OracleCon
        """
        return oracle_con.OracleCon()


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()