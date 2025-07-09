import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=(), db_path="users.db"):
        self.query = query
        self.params = params
        self.db_path = db_path
        self.conn = None
        self.result = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Execute the query with parameters
        cursor.execute(self.query, self.params)

        # Fetch all results
        self.result = cursor.fetchall()

        # Return the results to the with-block
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection when exiting the with-block
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as results:
        for row in results:
            print(row)
