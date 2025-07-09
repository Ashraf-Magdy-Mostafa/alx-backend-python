import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Use the connection as a context manager
        with sqlite3.connect('users.db') as conn:
            # Pass the connection to the decorated function
            return func(conn, *args, **kwargs)
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Usage
user = get_user_by_id(user_id=1)
print(user)
