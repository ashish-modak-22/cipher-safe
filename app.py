import sqlite3
import bcrypt
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64




def database_connect():

    # Establishes a connection with the SQLite database and returns the connection object
    connection = sqlite3.connect("database.db")
    return connection



def initialize_database():

    # Initialize the SQLite database by creating required tables if they do not already exist
    connection = database_connect()
    cursor = connection.cursor()

    # Create users table to store user authentication details
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        hashed_password TEXT       
    )
""")

    # Create user_data table to store encrypted user-specified data
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS user_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        encrypted_data TEXT,
        iv TEXT
    )
""")

    # Save database changes and close the connection
    connection.commit()
    connection.close()



def user_registration():

    # Handles new user registration by collecting user details, securely hashing the password, and preparing a database connection
    username = input("Enter the userID: ")
    password = input("Enter password: ")

    # Generate a secure hash of the user's password before storing it
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode()

    # Establish database connection to store user information
    connection = database_connect()
    cursor = connection.cursor()

    
    try:

        # Insert the new user's credentials into the users table
        cursor.execute(
            """ INSERT INTO users(username, hashed_password) VALUES(?,?)""",
            (username, hashed_password)
        )

        # Commit the transaction after successful insertion
        connection.commit()
        print("Your registration is done successfully!!")

    
    except Exception as e:

        # Handle registration errors (e.g., duplicate username)
        print("Registration failed! Username already exists!")
        print(e)

    # Close the database connection to release resources
    connection.close()



def user_login():

    # Authenticates a user by verifying the provided credentials against the stored password hash
    userName = input("Enter the username/ID: ")
    password = input("Enter the password: ")

    # Establish a database connection to retrieve user credentials
    connection = database_connect()
    cursor = connection.cursor()

    # Fetch the user's ID and stored password hash using the username
    cursor.execute(
        """ SELECT id, hashed_password FROM users WHERE username = ?""",
        (userName,)
    )

    user = cursor.fetchone()
    connection.close()

    # Return if the username does not exist
    if user is None:
        print("The given username is not found")
        return None
    
    user_id = user[0]
    stored_hash = user[1]

    # Verify the entered password against the stored hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode()):
        print("Login successful!!")
        return user_id
    else:
        print("Login unsuccessful! Please verify the given password")
        return None



def add_user_data(user_id):

    # Encrypts and store user-provided data securely in the database
    title = input("Enter the title of the data: ")
    secret = input("Enter the secret data: ")

    # Encrypt the secret data before storing it in the database
    encrypted_text, iv = encrypt_data(secret)

    # Establish a database connection
    connection = database_connect()
    cursor = connection.cursor()

    # Store the encrypted data along with its initialization vector (IV)
    cursor.execute(
        """ INSERT INTO user_data(user_id, title, encrypted_data, iv) VALUES(?,?,?,?)""",
        (user_id, title, encrypted_text, iv)
    )

    # Commit the transaction and close the database connection
    connection.commit()
    connection.close()

    print("Your data is saved into the database")



def show_user_data(user_id):

    # Retrives, decrypts and displays all data associated with the given user
    connection = database_connect()
    cursor = connection.cursor()

    # Fetch all encrypted records belonging to the specified user
    cursor.execute(
        """ SELECT title, encrypted_data, iv FROM user_data WHERE user_id=?""",
        (user_id,)
    )

    data_rows = cursor.fetchall()
    connection.close()

    # Return if no records are found for the user
    if len(data_rows) == 0:
        print("Oops! No data found")
        return
    
    print("\n--------------- Your saved data are -------------\n")

    # Decrypt and display each stored record
    for data_row in data_rows:

        title = data_row[0]
        encrypted_data = data_row[1]
        iv = data_row[2]

        decrypted_data = decrypt_data(encrypted_data, iv)

        print(f"Title: {title}")
        print(f"Secret data: {decrypted_data}")
        print("\n")


def user_data_menu(user_id):

    # Displays the user dashboard and handles data management operations until the user chooses to log out

    while True:
        print("\n------------- Press ------------------\n")
        print("1 to add data")
        print("2 to view the saved data")
        print("3 to Logout from the database")

        choice = int(input("Enter your choice: "))

        # Execute the selected operation
        if choice == 1:
            add_user_data(user_id)

        elif choice == 2:
            show_user_data(user_id)

        elif choice == 3: 
            print("Successfully logged out")
            break

        else:
            print("Wrong choice")


# Secret key used for AES encryption and decryption
key = b"ashishpythoncode"


def encrypt_data(plain_text):

    # Encrypts plaintext using AES-CBC and returns the encrypted data along with the initialization vector(IV)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(
        pad(plain_text.encode(), AES.block_size)
    )

    return (
        base64.b64encode(encrypted).decode(),
        base64.b64encode(iv).decode()
    )


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
