import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = F"{os.getcwd()}{os.sep}blue_dog.db"

# Blue Dogs

# creates a new user table if it doesn't exist
def create_user_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "users" (
            "user_id" INTEGER PRIMARY KEY,
            "count" INTEGER
        )
    """)

    connection.commit()
    connection.close()

# increments the blue dog count
def increase_blue_dogs(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT count
        FROM users
        WHERE (user_id = ?);
    """, (user_id,))

    result = cursor.fetchone()

    if (result == None):
        cursor.execute("""
            INSERT INTO users (user_id, count)
            VALUES (?, 1);
        """, (user_id,))

        connection.commit()
        connection.close()

        return 1
    
    cursor.execute("""
        UPDATE users
        SET count = ?
        WHERE (user_id = ?);
    """, (result[0]+1, user_id))

    connection.commit()
    connection.close()

    return result[0]+1

# handles getting the current blue dog count
def get_blue_dogs(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT count
        FROM users
        WHERE (user_id = ?);
    """, (user_id,))

    result = cursor.fetchone()
    if (result == None):
        return 0
     
    return result[0]

# handles getting the current blue dog count
def get_top_blue_dogs():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT count, user_id
        FROM users
        ORDER BY count
        DESC LIMIT 10
    """)

    result = cursor.fetchall()
    return result

def delete_blue_dog(user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE (user_id = ?)
    """, (user_id,))

    connection.commit()
    connection.close()

def set_blue_dog(user_id, count):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET count = ?
        WHERE user_id = ?
    """, (count, user_id))

    connection.commit()
    connection.close()

# Messages

# Create message table
def create_message_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "messages" (
            "id" INTEGER PRIMARY KEY
        )
    """)

    connection.commit()
    connection.close()

# Add message id to list
def add_message_id(id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (id)
        VALUES (?);
    """, (id,))


    connection.commit()
    connection.close()

def check_if_message_exists(id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1 FROM messages WHERE id = ? LIMIT 1
    """, (id,))

    exists = cursor.fetchone() is not None
    return exists
