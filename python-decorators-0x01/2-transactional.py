import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            return func(conn, *args, **kwargs)
    return wrapper


def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if no exception
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception so caller knows
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))


# Usage example
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully.")
except Exception as error:
    print(f"Failed to update email: {error}")
