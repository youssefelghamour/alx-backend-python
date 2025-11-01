#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a page of user data from the database"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    # Execute a query to fetch user data with LIMIT and OFFSET
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that simulates lazy pagination of user data"""
    offset = 0
    # Infinite loop to fetch pages until no more data is available
    while True:
        # Fetch a page of user data
        page = paginate_users(page_size, offset)
        # If the generator returns an empty page, break the loop
        if not page:
            break
        # Update the offset for the next page
        offset += page_size
        yield page