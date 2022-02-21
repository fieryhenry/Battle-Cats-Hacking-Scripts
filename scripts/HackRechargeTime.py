import sys
sys.path.append('..')
import helper

def find_offset(architecture):
    condtions_x86 = [0xF7, 0xE9, 0x89, 0xD0, 0xC1, 0xE8, 0x1F, 0xC1, 0xFA, 0x05, 0x01, 0xC2,
	0x01, 0xF2, 0x83, 0xFA, 0x3B, 0xB8, 0x3C, 0x00, 0x00, 0x00, 0x0F, 0x4F,
	0xC2, 0x8D, 0x65, 0xF4, 0x5E, 0x5F, 0x5B, 0x5D, 0xC3]

    condtions_x86_64 = []

    condtions_arm64_v8a = []

    condtions_armeabi_v7a = []

    offset = -1
    if architecture == "x86":
        offset = helper.find_offset(condtions_x86, - 169)
    elif architecture == "x86_64":
        offset = helper.find_offset(condtions_x86_64, -1)
    elif architecture == "arm64-v8a":
        offset = helper.find_offset(condtions_arm64_v8a, -1)
    elif architecture == "armeabi-v7a":
        offset = helper.find_offset(condtions_armeabi_v7a, -1)
    else:
        print("Error, your offset couldn't be searched for - please report his on discord or on github")
    return offset

def main_script(offset, session):

    print("Loading script...")
    helper.attach_interceptor_leave(offset, 0, session)

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