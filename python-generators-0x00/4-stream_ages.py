seed = __import__('seed')


def stream_user_ages():
    """Generator that streams user ages from the database"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    # Execute a query to fetch user ages
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()


def average_age():
    """Calculate the average age of users from the streamed ages"""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        return 0
    print(f"Average age of users: {total_age / count}")


if __name__ == "__main__":
    try:
        average_age()
    except BrokenPipeError:
        import sys
        sys.stderr.close()