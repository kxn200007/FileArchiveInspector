import sys
from subprocess import Popen, PIPE

# initialize variables
word_chosen = ""
history = list()
log_file_name = input("Enter the log file name: ")
mode = "START"

# set up pipes for communication with subprocesses
encrypt_process = Popen(['python', 'encrypt.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')
logger_process = Popen(['python', 'logger.py', log_file_name], stdout=PIPE, stdin=PIPE, encoding='utf8')

# send initial messages to logger
logger_process.stdin.write(log_file_name + "\n")
logger_process.stdin.write(mode + "\n")
logger_process.stdin.flush()

# prompt user for command and handle it
while True:
    # display available commands
    print("Commands: password | encrypt | decrypt | history | quit")
    mode = input("Enter a command: ")

    # handle history command
    if mode == "history":
        if len(history) == 0:
            print("History is empty.")
            continue
        i = 0
        while i != len(history):
            print(str(i + 1) + ". " + history[i])
            i += 1
        continue

    # handle quit command
    if mode == "quit":
        logger_process.stdin.write("QUIT")
        logger_process.stdin.flush()
        encrypt_process.stdin.write("QUIT")
        encrypt_process.stdin.flush()
        sys.exit()

    # handle encrypt, decrypt, and password commands
    encrypt_mode = ""
    if mode == "encrypt":
        encrypt_mode = "ENCRYPT"
    elif mode == "decrypt":
        encrypt_mode = "DECRYPT"
    elif mode == "password":
        encrypt_mode = "PASSKEY"
    else:
        print("Invalid command. Please try again.")
        continue

    # prompt user for word choice and send command to subprocesses
    choice = int(input("Choose from history:(1) | Create a new word:(2)\nEnter choice: "))
    if choice == 1:
        if len(history) == 0:
            print("Empty History")
            continue
        i = 0
        while i != len(history):
            print(str(i + 1) + ". " + history[i])
            i += 1
        index = input("Select a word: ")
        word_chosen = history[int(index) - 1]
    else:
        word_chosen = input("Enter your word: ")
        history.append(word_chosen)

    encrypt_mode += " " + word_chosen
    encrypt_process.stdin.write(encrypt_mode + "\n")
    encrypt_process.stdin.flush()
    logger_process.stdin.write(encrypt_mode + "\n")
    logger_process.stdin.flush()

    # read and display result from subprocess
    result = encrypt_process.stdout.readline().rstrip()
    if result != "":
        print(result + "\n")
    logger_process.stdin.write(result + "\n")
    logger_process.stdin.flush()