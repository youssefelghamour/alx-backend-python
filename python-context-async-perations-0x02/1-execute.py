import sqlite3


class DatabaseConnection:
    """Context manager for database connection"""
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def __enter__(self):
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

"""
# Using inheritance
class ExecuteQuery(DatabaseConnection):
    # Context manager for executing a database query
    def __init__(self, db_name, query, params=()):
        super().__init__(db_name)
        self.query = query
        self.params = params
    
    def __enter__(self):
        cursor = super().__enter__()
        cursor.execute(self.query, self.params)
        return cursor.fetchall()
    
    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
"""

# Using composition
class ExecuteQuery(DatabaseConnection):
    """Context manager for executing a database query"""
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.result = None
    
    def __enter__(self):
        # Use DatabaseConnection as a context manager internally
        with DatabaseConnection(self.db_name) as cursor:
            cursor.execute(self.query, self.params)
            self.result = cursor.fetchall()
        return self.result
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Nothing needed here because DatabaseConnection handles commit/close
        pass


# Example usage:
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        for row in results:
            print(row)