import sqlite3


class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_path)
        return self.conn  # Return the connection object to the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection when exiting the with-block
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db_path = "users.db"  # Your SQLite database file

    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        for row in results:
            print(row)
