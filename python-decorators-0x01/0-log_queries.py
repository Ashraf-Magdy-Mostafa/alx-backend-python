import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from keyword arguments or positional arguments
        query = kwargs.get('query', None)
        if query is None and args:
            # If query is passed positionally, assuming first argument is query
            query = args[0]

        # Log the SQL query before execution
        print(f"[{datetime.now()}] Executing SQL query: {query}")

        # Call the original function
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
users = fetch_all_users(query="SELECT * FROM users")
print(users)
