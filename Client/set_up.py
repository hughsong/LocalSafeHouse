import configparser

parser = configparser.ConfigParser()
parser.read('settings.ini')
print("[+]Start setting...")

PIN = input("Enter 4 digit PIN (You do not need to remember it): \n")

parser.add_section('folde_maze')
parser.set('folde_maze', 'PIN', PIN)
parser.set('folde_maze', 'application_name', '.LSH')

with open('settings.ini', 'w') as configfile:
    parser.write(configfile)

print("[+]Setup finished, please running command: python3 folder_maze.py")
