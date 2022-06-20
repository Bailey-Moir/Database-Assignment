# typing test, like bop it but with text, high scores, users
import random
import sqlite3 as sql
from time import time
import getpass

def cast(val_fn, fn):
    sucess = False
    final = fn(0)
    while not sucess:
        try:
            final = fn(val_fn())
        except ValueError:
            print("Wrong type of input, please try again.")
        else:
            sucess = True
    return final

def login():
    global uid
    # Get details
    inputted_username = input("username: ")
    inputted_password = getpass.getpass(prompt="password: ")

    # Query
    user_details = con.execute("""SELECT password, user_id
        FROM users
        WHERE username = ?
    """, [inputted_username]).fetchone()

    # Check if htey failed, if they didn't, see the session user.
    if (user_details == None or user_details[0] != inputted_password):
        print("Incorrect username or password.")
    else: uid = user_details[1]


con = sql.connect('typing-test.db')
cur = con.cursor()

# Whether the game should stop, i.e. whether it should stop going back to the main menu.
shouldQuit = False

while not shouldQuit:
    match cast(lambda: input("(1) Leaderboard\n(2) View User\n(3) Remove User\n(4) Remove Record\n(5) Quit\n"), int):
        case 1:
            # Query
            records = con.execute("""SELECT count, users.user_id, record_id, username
                FROM records
                INNER JOIN users on users.user_id = records.user_id
                ORDER BY records.count DESC
            """).fetchall()[:50]
            # Print all records
            for i in range(0,len(records)): 
                print(f'#{i + 1} {records[i][3]}: {records[i][0]} RECORD-ID: {records[i][2]}, USER-ID: {records[i][1]}') 

        case 2:
            # The user requested to view
            searched_user = input("Username of user: ")
            # Query
            records = con.execute("""SELECT count, users.user_id, record_id
                FROM records
                INNER JOIN users on users.user_id = records.user_id
                WHERE users.username = ?
                ORDER BY count DESC
            """, [searched_user]).fetchall()[:50]
            # Print user ID
            if (len(records) > 0): 
                print(f'USER-ID: {records[0][1]}')
                # Print all records
                for i in range(0, len(records)):
                    print(f'#{i + 1} {records[i][0]} RECORD-ID: {records[i][2]}')
        
        case 3:
            # Get details
            id_one = input("user id: ")
            id_two = input("re-enter user id: ")

            # If the two usernames are the same, delete hte user if it can be found.
            if (id_one == id_two):
                try:
                    con.execute("DELETE FROM users WHERE user_id = ?", [id_one])
                except:
                    print("User not found!")

        case 4:
            # Get details
            record_one = input("record id: ")
            record_two = input("re-enter record id: ")

            # If the two record ids are the same, delete the record if it can be found.
            if (record_one == record_two):
                try:
                    con.execute("DELETE FROM records WHERE record_id = ?", [record_one])
                except:
                    print("Record not found!")
                    
        case 5: shouldQuit = True

con.commit()
con.close()