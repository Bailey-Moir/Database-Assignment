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

con = sql.connect('typing-test.db')
cur = con.cursor()

# The session user
uid = -1;

# Whether the game should stop, i.e. whether it shuld stop going back to the main menu.
shouldQuit = False

while not shouldQuit:
    # TODO Admin delete, and change own password
    match cast(lambda: input("(1) Play\n(2) Leaderboard\n(3) View User\n(4) Create Account\n(5) Quit\n"), int):
        case 1:
            # If the user has not logged in yet in this session, get them to. If they fail, go back to menu.
            if uid == -1:
                # Get details
                inputted_username = input("username: ")
                inputted_password = getpass.getpass(prompt="password: ")

                # Query
                user_details = con.execute("""SELECT password, user_id
                    FROM users
                    WHERE username = :name
                """, [inputted_username]).fetchone()

                # Check if htey failed, if they didn't, see the session user.
                if (user_details == None or user_details[0] != inputted_password):
                    print("Incorrect username or password.")
                else: uid = user_details[1]

            # If the session user has been set, play the game
            if uid != -1:
                # All prompts the user can be prompted with
                PROMPTS = ["able", "acid", "aged", "also", "area", "army", "away", "baby", "back", "ball", "band", "bank", "base", "bath", "bear", "beat", "been", "beer", "bell", "belt", "best", "bill", "bird", "blow", "blue", "boat", "body", "bomb", "bond", "bone", "book", "boom", "born", "boss", "both", "bowl", "bulk", "burn", "bush", "busy", "call", "calm", "came", "camp", "card", "care", "case", "cash", "cast", "cell", "chat", "chip", "city", "club", "coal", "coat", "code", "cold", "come", "cook", "cool", "cope", "copy", "core", "cost", "crew", "crop", "dark", "data", "date", "dawn", "days", "dead", "deal", "dean", "dear", "debt", "deep", "deny", "desk", "dial", "dick", "diet", "disc", "disk", "does", "done", "door", "dose", "down", "draw", "drew", "drop", "drug", "dual", "duke", "dust", "duty", "each", "earn", "ease", "east", "easy", "edge", "else", "even", "ever", "evil", "exit", "face", "fact", "fail", "fair", "fall", "farm", "fast", "fate", "fear", "feed", "feel", "feet", "fell", "felt", "file", "fill", "film", "find", "fine", "fire", "firm", "fish", "five", "flat", "flow", "food", "foot", "ford", "form", "fort", "four", "free", "from", "fuel", "full", "fund", "gain", "game", "gate", "gave", "gear", "gene", "gift", "girl", "give", "glad", "goal", "goes", "gold", "Golf", "gone", "good", "gray", "grew", "grey", "grow", "gulf", "hair", "half", "hall", "hand", "hang", "hard", "harm", "hate", "have", "head", "hear", "heat", "held", "hell", "help", "here", "hero", "high", "hill", "hire", "hold", "hole", "holy", "home", "hope", "host", "hour", "huge", "hung", "hunt", "hurt", "idea", "inch", "into", "iron", "item", "jack", "jane", "jean", "john", "join", "jump", "jury", "just", "keen", "keep", "kent", "kept", "kick", "kill", "kind", "king", "knee", "knew", "know", "lack", "lady", "laid", "lake", "land", "lane", "last", "late", "lead", "left", "less", "life", "lift", "like", "line", "link", "list", "live", "load", "loan", "lock", "logo", "long", "look", "lord", "lose", "loss", "lost", "love", "luck", "made", "mail", "main", "make", "male", "many", "Mark", "mass", "matt", "meal", "mean", "meat", "meet", "menu", "mere", "mike", "mile", "milk", "mill", "mind", "mine", "miss", "mode", "mood", "moon", "more", "most", "move", "much", "must", "name", "navy", "near", "neck", "need", "news", "next", "nice", "nick", "nine", "none", "nose", "note", "okay", "once", "only", "onto", "open", "oral", "over", "pace", "pack", "page", "paid", "pain", "pair", "palm", "park", "part", "pass", "past", "path", "peak", "pick", "pink", "pipe", "plan", "play", "plot", "plug", "plus", "poll", "pool", "poor", "port", "post", "pull", "pure", "push", "race", "rail", "rain", "rank", "rare", "rate", "read", "real", "rear", "rely", "rent", "rest", "rice", "rich", "ride", "ring", "rise", "risk", "road", "rock", "role", "roll", "roof", "room", "root", "rose", "rule", "rush", "ruth", "safe", "said", "sake", "sale", "salt", "same", "sand", "save", "seat", "seed", "seek", "seem", "seen", "self", "sell", "send", "sent", "sept", "ship", "shop", "shot", "show", "shut", "sick", "side", "sign", "site", "size", "skin", "slip", "slow", "snow", "soft", "soil", "sold", "sole", "some", "song", "soon", "sort", "soul", "spot", "star", "stay", "step", "stop", "such", "suit", "sure", "take", "tale", "talk", "tall", "tank", "tape", "task", "team", "tech", "tell", "tend", "term", "test", "text", "than", "that", "them", "then", "they", "thin", "this", "thus", "till", "time", "tiny", "told", "toll", "tone", "tony", "took", "tool", "tour", "town", "tree", "trip", "true", "tune", "turn", "twin", "type", "unit", "upon", "used", "user", "vary", "vast", "very", "vice", "view", "vote", "wage", "wait", "wake", "walk", "wall", "want", "ward", "warm", "wash", "wave", "ways", "weak", "wear", "week", "well", "went", "were", "west", "what", "when", "whom", "wide", "wife", "wild", "will", "wind", "wine", "wing", "wire", "wise", "wish", "with", "wood", "word", "wore", "work", "yard", "yeah", "year", "your", "zero", "zone"]

                # Tutorial
                input("You have 1.5 second to type the prompt and click enter, if you fail, the run ends.\nPress enter to start...")

                # Number of prompts done correctly
                n = 0
                # Whether the user is still alive or not; if the run has failed yet.
                alive = True
                while alive:
                    # The prompt that will be used
                    pick = PROMPTS[random.randint(0, PROMPTS.__len__() - 1)]
                    # The time that the prompt was asked
                    inital = time()
                    
                    # Asks the quesiton
                    answer = input(pick + '\n').strip();

                    # If the prompt was asked more than a second ago or the answer isn't the as the prompt, then stop the loop.
                    if time() - inital > 1.5 or answer != pick: alive = False
                    else: n+=1

                # Print an X and then print the score.
                print(f'\nX \n{n}')

                con.execute("INSERT INTO records (count, user_id) VALUES (?, ?)", [n, uid])
        
        case 2:
            # Query
            records = con.execute("""SELECT count, records.user_id, username
                FROM records
                INNER JOIN users on users.user_id = records.user_id
                ORDER BY records.count DESC
            """).fetchall()[:50]
            # Print all records
            for i in range(0,len(records)): 
                print(f'#{i + 1} {records[i][2]}: {records[i][0]}') 

        case 3:
            # The user requested to view
            searched_user = input("Username of user: ")
            # Query
            records = con.execute("""SELECT count
                FROM records
                INNER JOIN users on users.user_id = records.user_id
                WHERE users.username = :name
                ORDER BY count DESC
            """, [searched_user]).fetchall()[:50]
            # Print all records
            for i in range(0, len(records)):
                print(f'#{i + 1} {records[i][0]}')
        
        case 4:
            username = input("username: ")
            password1 = getpass.getpass(prompt='password: ')
            password2 = getpass.getpass(prompt='re-enter password: ')

            if (password1 == password2):
                uid = con.execute("INSERT INTO users (username, password) VALUES (?, ?) RETURNING user_id", [username, password1]).fetchone()[0]
                print(f"Account '{username}' was created!")
            else:
                print("Passwords do not match.")

        case 5: shouldQuit = True

con.commit()
con.close()