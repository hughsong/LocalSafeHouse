# SOURCE FILE:    condif_reader.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      Write attributes into and obtain values from configuration file named “settings.ini”. 
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import configparser
import os
from random import randint
import math
config = configparser.ConfigParser()
config.read('settings.ini')
# xor
def str_xor(s1, s2):
	return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

# xor encryption used for encrypt user password or other string
def xor_encryption(content, key=None):
	if not key:
		key = str(randint(1000000, 9999999))
	multi = math.ceil(len(content)/len(key))
	xorKey = key*multi
	encrypted_content = str_xor(content, xorKey)
	return encrypted_content, key

# xor encryption used for decrypt user password or other string
def xor_decryption(content, key):
	multi = math.ceil(len(content)/len(key))
	xorKey = key*multi
	decrypted_content = str_xor(content, xorKey)
	return decrypted_content

# Setter function to write user’s information into the configuration file during user registration
def regi_insert(username,password,email_address,photo_key):
	config.add_section('USER')
	password, key = xor_encryption(password)
	config.set('USER', 'username', username)
	config.set('USER', 'password', password)
	config.set('USER', 'email_address', email_address)
	config.set('USER', 'key', key)
	config.set('USER', 'photo_key', photo_key)
	with open('settings.ini', 'w') as configfile:
		config.write(configfile)

# Setter function
def set_PIN(PIN):
	config['folde_maze']['PIN'] = PIN
	with open('settings.ini', 'w') as configfile:
		config.write(configfile)

# Getter: get the key for decrypting user photo
def get_photo_key():
	key = config['USER']['photo_key']
	return key

# Getter: get the corroct application folder path
def get_path():
	root_path=os.path.expanduser('~')
	app_name = get_app_name()
	user_dir = os.path.join(root_path,app_name)
	# PIN is the correct file path
	PIN = str(int(int(get_PIN())/222))
	# record correct program path
	destination_path = user_dir
	for i in PIN:
		destination_path=os.path.join(destination_path,i)
	return destination_path

# Getter: get the application name
def get_app_name():
	name = config['folde_maze']['application_name']
	return name

# Getter: get the username
def get_username():
	name = config['USER']['username']
	return name

# Getter: get the encrypted user password
def get_password():
	password = config['USER']['password']
	return password

# Getter: get the key for decrypting user password
def get_key():
	key = config['USER']['key']
	return key

# Getter: get the user emaill address
def get_email():
	email = config['USER']['email_address']
	return email

# Getter: get the PIN
def get_PIN():
	PIN = config['folde_maze']['PIN']
	return PIN
