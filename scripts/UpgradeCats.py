import sys
sys.path[0] += ('\..')
import helper

def find_offsets(architecture):
    condtions_x86 = [0x0F, 0xB6, 0xC2, 0xC1, 0xE0, 0x08, 0x0F, 0xB6, 0xF9, 0x09, 0xC7, 0x0F,
	0xB6, 0xC5, 0xC1, 0xE0, 0x10, 0x09, 0xC7, 0x0F, 0xB6, 0xC6, 0xC1, 0xE0,
	0x18, 0x09, 0xC7, 0x8B, 0x45, 0x0C, 0x39, 0xC7, 0x89, 0xC7, 0x7D, 0x58,
	0xE8]

    condtions_x86_64 = []

    condtions_arm64_v8a = []

    condtions_armeabi_v7a = []

    offset = -1
    if architecture == "x86":
        offset = helper.find_offset(condtions_x86, - 92, True)
    elif architecture == "x86_64":
        offset = helper.find_offset(condtions_x86_64, - 1)
    elif architecture == "arm64-v8a":
        offset = helper.find_offset(condtions_arm64_v8a, - 1)
    elif architecture == "armeabi-v7a":
        offset = helper.find_offset(condtions_armeabi_v7a, - 1)
    else:
        print("Error, your offset couldn't be searched for - please report his on discord or on github")
    return offset

def get_plus_base(input):
    split = input.split("+")
    base = ""
    plus = ""
    if split[0]:
        base = helper.validate_int(split[0])
    if split[1]:
        plus = helper.validate_int(split[1])
    return [base, plus]

def get_cats():
    user_input = input("Enter cat ids separated by spaces (or a - between 2 ids to make a range(inclusive)):\n")
    ids = helper.get_range(user_input)
    all_at_once = ""
    if len(ids) == 1:
        all_at_once = "2"
    else:
        all_at_once = input("Do you want to edit them all at once(1), or individually?(2):\n")
    first = True
    plus = ""
    base = ""

    base_calls = ""
    plus_calls = ""

    for id in ids:
        if all_at_once == "1" and first:
            levels = get_plus_base(input(f"Enter the base level followed by a \"+\" then the plus level, e.g 5+12. If you want to ignore the base level do +12, if you want to ignore the plus level do 5+:\n"))
            base = levels[0]
            plus = levels[1]
            first = False
        elif all_at_once == "2" or first:
            levels = get_plus_base(input(f"For cat {id}: Enter the base level followed by a \"+\" then the plus level, e.g 5+12. If you want to ignore the base level do +12, if you want to ignore the plus level do 5+:\n"))
            base = levels[0]
            plus = levels[1]
        if base != "null":
            base_calls += helper.create_function_calls([id, base])
        if plus != "null":
            plus_calls += helper.create_function_calls([id, plus])
    return [base_calls, plus_calls]


def main_script(offsets, session):
    cats = get_cats()
    
    print("Loading script...")
    function_base = cats[0]
    functions_plus = cats[1]

    helper.call_native_function(offsets[0], session, function_base, "void", "['int', 'int']")
    helper.call_native_function(offsets[1], session, functions_plus, "void", "['int', 'int']")

    print("Success")
def main():
    print("Warning architectures other than x86 have not been tested on this script, so they may not work\nThe game may crash if you are in the upgrade menu while editing")
    data = helper.pull_file()

    architecture = data[0]
    game_version = data[1]

    print("Finding function offset...")
    offsets = find_offsets(architecture)

    print("Creating session...")
    session = helper.create_session(game_version)
    main_script(offsets, session)
main()