import sys
sys.path[0] += ('\..')
import helper

def find_offset(architecture):
    condtions_x86 = [0x08, 0x8A, 0x70, 0x09, 0x32, 0x70, 0x06, 0x32, 0x68, 0x07, 0x0F, 0xB6,
	0xF5, 0xC1, 0xE6, 0x18, 0x0F, 0xB6, 0xFE, 0xC1, 0xE7, 0x10, 0x0F, 0xB6,
	0xD2, 0xC1, 0xE2, 0x08, 0x0F, 0xB6, 0xC1, 0x09, 0xD0, 0x09, 0xF8, 0x09,
	0xF0, 0x8D, 0x65, 0xF8, 0x5E, 0x5F, 0x5D, 0xC3]

    condtions_x86_64 = [0x0F, 0xB6, 0xD2, 0xC1, 0xE2, 0x18, 0x0F, 0xB6, 0xF8, 0xC1, 0xE7, 0x10,
	0x0F, 0xB6, 0xC9, 0xC1, 0xE1, 0x08, 0x40, 0x0F, 0xB6, 0xC6, 0x09, 0xC8,
	0x09, 0xF8, 0x09, 0xD0, 0xC3]

    condtions_arm64_v8a = [0x20, 0x01, 0x08, 0x4A, 0x68, 0x01, 0x0A, 0x4A, 0xA9, 0x01, 0x0C, 0x4A,
	0x00, 0x1D, 0x18, 0x33, 0xEA, 0x01, 0x0E, 0x4A, 0x20, 0x1D, 0x10, 0x33,
	0x40, 0x1D, 0x08, 0x33, 0xC0, 0x03, 0x5F, 0xD6]

    condtions_armeabi_v7a = []

    offset = -1
    if architecture == "x86":
        offset = helper.find_offset(condtions_x86, - 25)
    elif architecture == "x86_64":
        offset = helper.find_offset(condtions_x86_64, - 26)
    elif architecture == "arm64-v8a":
        offset = helper.find_offset(condtions_arm64_v8a, - 1)
    elif architecture == "armeabi-v7a":
        offset = helper.find_offset(condtions_armeabi_v7a, - 1)
    else:
        print("Error, your offset couldn't be searched for - please report his on discord or on github")
    return offset

def main_script(offset, session):
    money = helper.validate_int(input("How much money do you want to set?:\n"))
    if money == "null":
        print("Please enter a valid number")
        main_script(offset, session)
    print("Loading script...")
    helper.attach_interceptor_leave(offset, money*100, session)

    print("Success\nYou must keep this script running for the hack to work")
    sys.stdin.read()
def main():
    print("Warning architectures other than x86 have not been tested on this script, so they may not work")
    data = helper.pull_file()

    architecture = data[0]
    game_version = data[1]

    print("Finding function offset...")
    offset = find_offset(architecture)

    print("Creating session...")
    session = helper.create_session(game_version)
    main_script(offset, session)
main()