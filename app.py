import sqlite3
import bcrypt
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


def database_connect():
    connection = sqlite3.connect("database.db")
    return connection


# Database initializer function ---> It initializes the registration and login database for the user ....
def initialize_database():
    connection = database_connect()
    cursor = connection.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        hashed_password TEXT       
    )
""")
    
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS user_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        encrypted_data TEXT,
        iv TEXT
    )
""")
    
    connection.commit()
    connection.close()


# User registration database ---> creates database for userIDs and encrypted passwords
def user_registration():
    username = input("Enter the userID: ")
    password = input("Enter password: ")

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()
    
    connection = database_connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """ INSERT INTO users(username, hashed_password) VALUES(?,?)""",
            (username, hashed_password)
        )

        connection.commit()
        print("Your registration is done successfully!!")

    except Exception as e:
        print("Registration failed! Username already exists!")
        print(e)

    connection.close()


# User login 
def user_login():
    userName = input("Enter the username/ID: ")
    password = input("Enter the password: ")

    connection = database_connect()
    cursor = connection.cursor()

    cursor.execute(
        """ SELECT id, hashed_password FROM users WHERE username = ?""",
        (userName,)
    )

    user = cursor.fetchone()
    connection.close()

    if user is None:
        print("The given username is not found")
        return None
    
    user_id = user[0]
    stored_hash = user[1]

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode()):
        print("Login successful!!")
        return user_id
    else:
        print("Login unsuccessful! Please verify the given password")
        return None


# Adding the user data ...
def add_user_data(user_id):
    title = input("Enter the title of the data: ")
    secret = input("Enter the secret data: ")

    encrypted_text, iv = encrypt_data(secret)

    connection = database_connect()
    cursor = connection.cursor()

    cursor.execute(
        """ INSERT INTO user_data(user_id, title, encrypted_data, iv) VALUES(?,?,?,?)""",
        (user_id, title, encrypted_text, iv)
    )

    connection.commit()
    connection.close()

    print("Your data is saved into the database")


# Viewing the stored data ....
def show_user_data(user_id):
    connection = database_connect()
    cursor = connection.cursor()

    cursor.execute(
        """ SELECT title, encrypted_data, iv FROM user_data WHERE user_id=?""",
        (user_id,)
    )

    data_rows = cursor.fetchall()
    connection.close()

    if len(data_rows) == 0:
        print("Oops! No data found")
        return
    
    print("\n--------------- Your saved data are -------------\n")
    
    for data_row in data_rows:

        title = data_row[0]
        encrypted_data = data_row[1]
        iv = data_row[2]

        decrypted_data = decrypt_data(encrypted_data, iv)

        print(f"Title: {title}")
        print(f"Secret data: {decrypted_data}")
        print("\n")


def user_data_menu(user_id):

    while True:
        print("\n------------- Press ------------------\n")
        print("1 to add data")
        print("2 to view the saved data")
        print("3 to Logout from the database")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_user_data(user_id)

        elif choice == 2:
            show_user_data(user_id)

        elif choice == 3: 
            print("Successfully logged out")
            break

        else:
            print("Wrong choice")


# The AES 16 bytes key generation for encryption...
key = b"ashishpythoncode"


# Encryption .....
def encrypt_data(plain_text):
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(
        pad(plain_text.encode(), AES.block_size)
    )

    # FIXED (tuple, NOT set)
    return (
        base64.b64encode(encrypted).decode(),
        base64.b64encode(iv).decode()
    )


# Decryption ...
def decrypt_data(encrypted_text, iv):

    encrypted_text = base64.b64decode(encrypted_text)
    iv = base64.b64decode(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(
        cipher.decrypt(encrypted_text),
        AES.block_size
    )

    return decrypted.decode()


def main():

    initialize_database()

    while True:
        print("\n-------------- Press -------------\n")
        print("1 to Register")
        print("2 to Login")
        print("3 to Exit")

        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            user_registration()

        elif choice == 2:
            user_id = user_login()

            if user_id:
                print("You can now store your data.......")
                print(f"User Id No. : {user_id}")
                user_data_menu(user_id)

        elif choice == 3:
            print("Exiting the process.......")
            break

        else:
            print("Invalid choice! Please check your options")

main()
