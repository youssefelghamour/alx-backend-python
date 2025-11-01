seed = __import__('seed')


def stream_users_in_batches(batch_size):
    """Generator function that yields user data in batches of specified size"""
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    """
    # With fetchmany: more efficient
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch
    """

    batch = []
    for row in cursor:
        batch.append({
            'user_id': row['user_id'],
            'name': row['name'],
            'email': row['email'],
            'age': int(row['age'])
        })
        if len(batch) == batch_size:
            yield batch
            batch = []
    
    # The last batch might be smaller if it didn't fill up
    if batch:
        yield batch
    
    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Generator function that yields user data in batches of specified size for users older than 25"""
    batch = next(stream_users_in_batches(batch_size))

    result = [user for user in batch if user['age'] > 25]
    yield result