import time
import sqlite3 
import functools

def retry_on_failure(retries=3, delay=2):  # takes arguments
    def decorator(func): 
        """A decorator that retries a function upon failure for a specified number of attempts with a delay"""
        @functools.wraps(func)
        def wrapper(conn, *args, retries=3, delay=2, **kwargs):
            for _ in range(retries):
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def with_db_connection(func):
    """A decorator that automatically handles opening and closing database connections""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)