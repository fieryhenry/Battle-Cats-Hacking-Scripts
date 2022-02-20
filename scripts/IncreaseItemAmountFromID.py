import sys
sys.path.append('..')
import helper

def get_items():
    user_input = input("Enter item ids separated by spaces (or a - between 2 ids to make a range(inclusive)):\n")
    ids = helper.get_range(user_input)
    output = ""
    all_at_once = ""
    if len(ids) == 1:
        all_at_once = "2"
    else:
        all_at_once = input("Do you want to edit them all at once(1), or individually?(2):\n")
    first = True
    amount = 0
    for id in ids:
        if all_at_once == "1" and first:
            amount = helper.validate_int(input(f"Enter the item amount:\n"))
            first = False
        elif all_at_once == "2" or first:
            amount = helper.validate_int(input(f"Enter the item amount for item: {id}:\n"))
        if amount == "null":
            print("Please enter a valid number")
            continue
        output += helper.create_function_calls([id, amount, 0])
    return output

def find_offset():
    condtions = [0x0F, 0xB6, 0xF5, 0xC1, 0xE6, 0x18, 0x0F, 0xB6, 0xCE, 0xC1, 0xE1, 0x10,
	0x0F, 0xB6, 0xD2, 0xC1, 0xE2, 0x08, 0x0F, 0xB6, 0x44, 0x24, 0x17, 0x09,
	0xD0]
    return helper.find_offset(condtions, - 141)

def main_script(offset, session):
    items = get_items()

    print("Loading script...")

    helper.create_script(offset, session, items, "void", "['int', 'int', 'int']")

    print("Success.\nYou need to enter another menu in game for your edits to save")
    user_input = input('Type "exit" to exit or press enter to edit more items:')
    if user_input != "exit":
        main_script(offset, session)
def main():
    print("Currently this script only works with x86 architecture")
    helper.pull_file()

    print("Finding function offset...")
    offset = find_offset()

    print("Creating session...")
    session = helper.create_session()
    main_script(offset, session)
main()