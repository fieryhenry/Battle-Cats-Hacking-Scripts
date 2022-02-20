import frida
import os
import subprocess

def find_offset(byte_conditons, end_offset):
    if not os.path.exists("../libnative-lib.so"):
        print("Error libnative-lib.so file not found")
        exit()
    lib = open("../libnative-lib.so", "rb").read()

    search = bytes(byte_conditons)
    index = lib.find(search)

    if index < 0:
        print("Error, address not found")
        exit()    

    return index + end_offset

def create_session(game_version):
    try:
        process_name = "The Battle Cats"
        if game_version == "jp":
            process_name = "にゃんこ大戦争"
        session = frida.get_usb_device(1).attach(process_name)
    except frida.ServerNotRunningError:
        print("Please start the frida server")
        exit()
    return session
def adb_pull(package_name, architecture):
    lib_path = f"/data/app/{package_name}/lib/{architecture}/libnative-lib.so"
    return_code = subprocess.run(f"adb pull {lib_path} ..", capture_output=True).returncode
    return return_code

def create_script(offset, session, function_calls, return_type, perameters):
    script = session.create_script(f"let f = new NativeFunction(Module.findBaseAddress('libnative-lib.so').add({offset}), '{return_type}', {perameters});\n{function_calls}")
    script.load()

def find_package_name(game_version):
    output = str(subprocess.run(f"adb shell ls /data/app/", capture_output=True).stdout)
    index = output.find(f"jp.co.ponos.battlecats{game_version}")
    return output[index:index+24+len(game_version)]

def find_architecture(package_name):
    output = subprocess.run(f"adb shell ls /data/app/{package_name}/lib/", capture_output=True).stdout
    return str(output)[2:-5]

def pull_file():
    game_version = input("What game version are you running (e.g: en, jp, kr, tw):")
    if game_version == "jp":
        game_version = ""
    
    package_name = find_package_name(game_version)
    architecture = find_architecture(package_name)

    print("Loading libnative-lib.so file...")
    
    return_code = adb_pull(package_name, architecture)
    if return_code == 1:
        print("Error, libnative-lib.so file not found")
        exit()
    if game_version == "": game_version = "jp"
    return [architecture, game_version]


def validate_int(input):
    if input.startswith("-") and input[1:].isdigit() or input.isdigit():
        return int(input)
    else:
        return "null"


def get_range(input):
    ids = []
    if "-" in input:
        content = input.split('-')
        first = validate_int(content[0])
        second = validate_int(content[1])
        if first == "null" or second == "null":
            print(f"Please enter 2 valid numbers when making a range : {first} | {second}")
            return []
        ids = range(first, second+1)
    else:
        content = input.split(" ")
        for id in content:
            item_id = validate_int(id)
            if item_id == "null":
                print(f"Please enter a valid number : {id}")
                continue
            ids.append(item_id)
    return ids

def create_function_calls(perameters):
    output = "f("
    for perameter in perameters:
        output += f"{perameter}, "
    output += ");\n"
    return output
