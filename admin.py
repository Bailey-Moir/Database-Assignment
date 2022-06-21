# typing test, like bop it but with text, high scores, users
import random
import sqlite3 as sql
from time import time
import getpass
import hashlib

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

inputted_admin_password = hashlib.sha256(getpass.getpass(prompt="password: ").encode()).hexdigest()
admin_pass = '0876dfca6d6fedf99b2ab87b6e2fed4bd4051ede78a8a9135b500b2e94d99b88'

if (admin_pass != inputted_admin_password):
    print("Access Denied.")
else:
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
                if (con.execute("""SELECT 1
                    FROM users
                    WHERE users.user_id = ?
                """, [id_one]).fetchone() == None):
                    print ("User not found!")
                elif (id_one != id_two):
                    print("IDs do not match.")
                else:
                    con.execute("DELETE FROM users WHERE user_id = ?", [id_one])
                    print("User deleted.")

            case 4:
                # Get details
                record_one = input("record id: ")
                record_two = input("re-enter record id: ")

                # If the two record ids are the same, delete the record if it can be found.
                if (con.execute("""SELECT 1
                    FROM records
                    WHERE records.record_id = ?
                """, [record_one]).fetchone() == None):
                    print ("Record not found!")
                elif (record_one != record_two):
                    print("IDs do not match.")
                else:
                    con.execute("DELETE FROM records WHERE record_id = ?", [record_one])
                    print("Record deleted.")
                        
            case 5: shouldQuit = True

    con.commit()
    con.close()