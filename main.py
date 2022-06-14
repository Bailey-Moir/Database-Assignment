# typing test, like bop it but with text, high scores, users
import random
import sqlite3
from time import time

# All prompts the user can be prompted with
PROMPTS = ["bap","boop","beep"]

# Tutorial
print("You have 1 second to type what prompt and click enter, if you fail, the run ends.")
input("Press enter to start...")

# Number of prompts done correctly
n = 0
# Whether the user is still alive or not; if the run has failed yet.
alive = True
while alive:
    # The prompt that will be used
    pick = PROMPTS[random.randint(0, 2)]
    # The time that the prompt was asked
    inital = time()
    
    # Asks the quesiton
    answer = input(pick + '\n')

    # If the prompt was asked more than a second ago or the answer isn't the as the prompt, then stop the loop.
    if time() - inital > 1 or answer != pick: alive = False
    else: n+=1

# Print an X and then print the score.
print(f'X \n{n}')
