import sys
sys.path.append("..")
from src.commands import enter, create, take, put, exit_, state, item

args_count = {"enter": 2, "create": 3, "take": 3, "put": 3, "exit": 2, "state": 1, "item": 3}
methods = {"enter": enter, "create": create, "take": take, "put": put, "exit": exit_, "state": state, "item": item}
arg_types = {"enter": [int], "create": [int, float], "take": [int, int], "put": [int, int], "exit": [int], "item": [int, float]}

def print_commands():
    print("Available commands are:")
    print("'enter ID' - client entering the store (unique ID of type int)")
    print("'create ID CREDITS' - create client and assign him some credits (unique ID of type int, CREDITS of type float)")
    print("'take ID Item_ID' - client taking Item_ID (unique ID of type int, unique Item_ID of type int)")
    print("'put ID Item_ID' - client returning Item_ID onto the shelf (unique ID of type int, unique Item_ID of type int)")
    print("'exit ID' - client exiting the store (unique ID of type int)")
    print("'state' - display stores state")
    print("'item Item_ID PRICE' - add new item to the store (unique Item_ID of type int, PRICE of type float)")
    print("'quit' - close the cli (erases the db)")
    print("'commands' - prints these instructions")

def parse(command: str):
    command = command.split(" ")
    try:
        arg_num = args_count[command[0]]
        if arg_num != len(command):
            print("invalid command")
            return None
        else:
            if len(command) > 1:
                try:
                    for i in range(len(command[1:])):
                        typee = arg_types[command[0]][i]
                        command[i+1] = typee(command[i+1])
                except ValueError:
                    print("invalid argument")
                    return None
            command[0] = methods[command[0]]
            return command
    except KeyError:
        print("invalid command")
        return None
    

if __name__ == "__main__":
    print("\n\n\n")
    print("THIS IS A SIMPLE CLI FOR TESTING THE MOCK STORE BACKEND.")
    print("\n\n")
    print_commands()
    print("\n")

    while(True):
        command = input(">>> ")
        if command == "quit":
            break
        if command == "commands":
            print_commands()
            continue
        parsed = parse(command)
        if parsed is None:
            continue
        parsed[0](*parsed[1:])
