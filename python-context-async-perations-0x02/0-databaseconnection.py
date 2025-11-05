import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def __enter__(self):
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

# Example usage:
if __name__ == "__main__":
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)