import sys
from typing import List
import signal
import os

def main():
    env = {}

    # Register keyboard interrupt handler
    def keyboardInterruptHandler(signal, frame):
        print("interrupted")
        sys.exit(0)

    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # Begin reading user input
    while True:
        # print("--")
        user_input = sys.stdin.readline()

        if user_input == "":  # EOF
            print("** You are now leaving shbenshel. Come back soon! **")
            break

        user_input = user_input.rstrip("\n")
        args = user_input.split(" ")

        # Builtins
        if handle_builtin(args):
            continue

        # Programs
        pid_or_exit_code = os.fork()
        if pid_or_exit_code == 0:
            os.execvpe(args[0], args, env)
        elif pid_or_exit_code > 0:
            os.waitpid(pid_or_exit_code, 0)


def handle_builtin(args: List[str]) -> bool:
    """
    Returns True if the input is a builtin, false if it isn't
    """
    if args[0] == "exit":
        sys.exit(0)
    elif args[0] == "cd":
        path = args[1]
        os.chdir(path)
        return True

    return False

main()
