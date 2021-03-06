import sys
sys.path[0] += ('\..')
import helper

def find_offset(architecture):
    condtions_x86 = [0xF7, 0xE9, 0x89, 0xD0, 0xC1, 0xE8, 0x1F, 0xC1, 0xFA, 0x05, 0x01, 0xC2,
	0x01, 0xF2, 0x83, 0xFA, 0x3B, 0xB8, 0x3C, 0x00, 0x00, 0x00, 0x0F, 0x4F,
	0xC2, 0x8D, 0x65, 0xF4, 0x5E, 0x5F, 0x5B, 0x5D, 0xC3]

    condtions_x86_64 = [0x48, 0x89, 0xC8, 0x48, 0xC1, 0xE8, 0x3F, 0x48, 0xC1, 0xF9, 0x25, 0x01,
	0xC1, 0x01, 0xD9, 0x83, 0xF9, 0x3B, 0xB8, 0x3C, 0x00, 0x00, 0x00, 0x0F,
	0x4F, 0xC1, 0x5B, 0x41, 0x5E, 0x5D, 0xC3]

    condtions_arm64_v8a = [0x89, 0xC2, 0xB5, 0x72, 0x6A, 0x02, 0x08, 0x4B, 0x08, 0x7C, 0x08, 0x1B,
	0x08, 0x7D, 0x29, 0x9B, 0x09, 0xFD, 0x7F, 0xD3, 0x08, 0xFD, 0x65, 0x93,
	0x08, 0x01, 0x09, 0x0B, 0xFD, 0x7B, 0x42, 0xA9, 0xF4, 0x4F, 0x41, 0xA9,
	0x08, 0x01, 0x0A, 0x0B, 0x1F, 0xF1, 0x00, 0x71, 0x89, 0x07, 0x80, 0x52,
	0x00, 0xC1, 0x89, 0x1A, 0xF6, 0x57, 0xC3, 0xA8, 0xC0, 0x03, 0x5F, 0xD6]

    condtions_armeabi_v7a = [0x10, 0xF1, 0x50, 0xE7, 0x05, 0x10, 0x44, 0xE0, 0xC0, 0x22, 0xA0, 0xE1,
	0xA0, 0x0F, 0x82, 0xE0, 0x01, 0x00, 0x80, 0xE0, 0x3C, 0x00, 0x50, 0xE3,
	0x3C, 0x00, 0xA0, 0xD3, 0x70, 0x8C, 0xBD, 0xE8]

    offset = -1
    if architecture == "x86":
        offset = helper.find_offset(condtions_x86, - 169)
    elif architecture == "x86_64":
        offset = helper.find_offset(condtions_x86_64, - 125)
    elif architecture == "arm64-v8a":
        offset = helper.find_offset(condtions_arm64_v8a, - 148)
    elif architecture == "armeabi-v7a":
        offset = helper.find_offset(condtions_armeabi_v7a, - 140)
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