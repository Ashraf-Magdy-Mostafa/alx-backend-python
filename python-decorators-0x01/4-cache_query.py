import time
import sqlite3
import functools

query_cache = {}


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            return func(conn, *args, **kwargs)
    return wrapper


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Use query string as cache key
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        # If not cached, execute the query and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Usage example:


# First call - executes query and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call - fetches result from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
