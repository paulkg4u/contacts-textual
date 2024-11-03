import pathlib
import sqlite3


DATABASE_PATH = pathlib.Path('.')/'contacts.db'


class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_table()

    def _create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        );
        """
        self._run_query(query)

    def _run_query(self, query, *query_args):
        result = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return result

    def get_all_contacts(self):
        result = self._run_query("SELECT * FROM contacts;")
        return result.fetchall()

    def get_last_contact(self):
        result = self._run_query(
            "SELECT * FROM contacts ORDER BY id DESC LIMIT 1;"
        )
        return result.fetchone()

    def add_contact(self, contact):
        print(contact)
        print(*contact)
        result = self._run_query(
            "INSERT INTO contacts VALUES (NULL, ?, ?, ?);",
            *contact
        )

    def delete_contact(self, contact_id):
        self._run_query("DELETE FROM contacts WHERE id = ?;", contact_id)

    def clear_contacts(self):
        self._run_query("DELETE FROM contacts;")
