# Python Generators

## Overview

This project demonstrates advanced usage of Python generators to handle large datasets efficiently, process data in batches, simulate live updates, and perform memory-efficient computations. It focuses on the `yield` keyword to provide iterative access to data, improving performance in data-driven applications.

## Files
| File | Description |
|------|-------------|
| `seed.py` | Sets up MySQL database `ALX_prodev`, creates `user_data` table, and seeds data from CSV. |
| `0-stream_users.py` | Generator function `stream_users()` to fetch rows one by one from `user_data`. |
| `1-batch_processing.py` | Functions `stream_users_in_batches(batch_size)` and `batch_processing(batch_size)` to process users in batches. |
| `2-lazy_paginate.py` | Implements `lazy_paginate(page_size)` and `paginate_users(page_size, offset)` for lazy loading paginated data. |
| `4-stream_ages.py` | Generator `stream_user_ages()` and function to compute average age memory-efficiently. |
| `0-main.py`, `1-main.py`, `2-main.py`, `main.py` | Example scripts to run and test generators. |

## Usage
1. Run `main.py` to create the database and seed data.
2. Use `0-main.py` to stream users one by one.
3. Use `1-main.py` to process users in batches.
4. Use `2-main.py` to lazily paginate data.
5. Use `4-stream_ages.py` to calculate average age efficiently.