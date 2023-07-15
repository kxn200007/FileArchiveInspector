import sys
import datetime

filename = input("Enter log file name: ").strip()

try:
    # open log file in append mode
    with open(filename, 'a') as f:
        # set initial mode and write start message to log file
        mode = "START"
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} [{mode}] Logging Started.\n")
        f.flush()

        # continue logging until user quits
        while mode != "QUIT":
            # read user input from stdin
            log_messages = sys.stdin.readline().rstrip()
            data = log_messages.split()
            mode = data[0]

            # check if user has quit
            if mode == "QUIT":
                break

            # extract message and write to log file
            MESSAGE = " ".join(data[1:]).rstrip()
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} [{mode}] {MESSAGE}\n")
            f.flush()

        # write stop message to log file
        message = f"{datetime.datetime.now():%Y-%m-%d %H:%M} [STOP] Logging Stopped.\n"
        f.write(message)
        f.flush()
except Exception as e:
    print(f"Error occurred while logging: {e}")
    sys.exit(1)