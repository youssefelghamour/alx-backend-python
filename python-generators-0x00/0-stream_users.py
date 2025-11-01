seed = __import__('seed')


def stream_users():
    """Generator that fetchs rows one by one from the user_data table in the ALX_prodev database"""
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield {
            'user_id': row['user_id'],
            'name': row['name'],
            'email': row['email'],
            'age': int(row['age'])
        }
    
    cursor.close()
    conn.close()