# SOURCE FILE:    file_encryption.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      1. cryptography
#				  2. pyAesCrypt encryption
#				  3. RSA encryption
#				  4. XOR encryption
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
from cryptography.fernet import Fernet
from config_reader import *
from pathlib import Path
from random import randint
import os, sys
import pyAesCrypt
import rsa
import math
import smtplib
import pyotp
from email.message import EmailMessage

# Generating the key file for cryptography encryption
def genwrite_key():
	num = randint(1000000, 9999999) 
	path = get_path()
	key_name = str(num) + ".key"
	key_path = path + "/key/" + key_name
	key = Fernet.generate_key()
	with open(key_path, "wb") as key_file:
		key_file.write(key)
	return key_name

# Function to load the key
def call_key(keyname):
	return open(keyname, "rb").read()

# using cryptography key file to encrypt file content and overwrite the old file
def cryptography_encrypt(file_name):
	key_name = genwrite_key()
	path = get_path()
	key_path = path + "/key/" + key_name
	key = call_key(key_path)
	file_content = Path(file_name).read_text()
	file_content = file_content.encode()
	a = Fernet(key)
	encrypted_content = a.encrypt(file_content)
	with open(file_name, "wb") as myfile:
		myfile.write(encrypted_content)
	return key_name

# using cryptography key file to decrypt it cypher and overwrite the encrypted file
# key file will be deleted after the file is successfully decrypted.
def cryptography_decrypt(file_name, key_name):
	path = get_path()
	key_path = path + "/key/" + key_name
	key = call_key(key_path)
	b = Fernet(key)
	file_content = open(file_name, "rb").read()
	decoded_content = b.decrypt(file_content)
	with open(file_name, "w") as myfile:
		myfile.write(decoded_content.decode())
	os.system("rm "+ key_path)

# pyAesCrypt encryption
def aes_encrypt(file_name):
	# encryption/decryption buffer size - 128K
	bufferSize = 128 * 1024
	password = str(randint(1000000, 9999999))
	# encrypt
	pyAesCrypt.encryptFile(file_name, file_name+".aes", password, bufferSize)
	return password

def aes_decrypt(file_name, password):
	filename = file_name+".aes"
	# encryption/decryption buffer size - 128K
	bufferSize = 128 * 1024
	# decrypt
	pyAesCrypt.decryptFile(filename, file_name, password, bufferSize)

# RSA encryption: generate a pair of keys (public key & private key)
def rsa_generateKeys():
	path = get_path()
	num = randint(1000000, 9999999) 
	public_key_name = "pu"+str(num) + ".pem"
	private_key_name = "pr"+str(num) + ".pem"
	(publicKey, privateKey) = rsa.newkeys(4096)
	with open(path+"/key/"+public_key_name, 'wb') as p:
		p.write(publicKey.save_pkcs1('PEM'))
	with open(path+"/key/"+private_key_name, 'wb') as p:
		p.write(privateKey.save_pkcs1('PEM'))
	return public_key_name, private_key_name

# RSA encryption: load rsa key
def load_rsa_Key(keyname, sign):
	path = get_path()
	if sign == "public":
		with open(path+"/key/" + keyname, 'rb') as p:
			key = rsa.PublicKey.load_pkcs1(p.read())
	else:
		with open(path+"/key/" + keyname, 'rb') as p:
			key = rsa.PrivateKey.load_pkcs1(p.read())
	return key

# RSA encryption: Using public key to encrypt the target file
def rsa_encrypt(file_name):
	path = get_path()
	public_key_name, private_key_name = rsa_generateKeys()
	key = load_rsa_Key(public_key_name,"public")
	file_content = Path(file_name).read_text()
	encrypted_content = rsa.encrypt(file_content.encode('ascii'), key)

	with open(file_name, "wb") as myfile:
		myfile.write(encrypted_content)

	os.system("rm "+ path+"/key/" +public_key_name)
	return private_key_name

# RSA encryption: Using private key to decrypt the cypher file
def rsa_decrypt(file_name, keyname):
	path = get_path()
	key = load_rsa_Key(keyname,"private")
	file_content = ""
	with open(file_name, 'rb') as f:
	    # do things with your file
	    file_content = f.read()
	decrypted_content = rsa.decrypt(file_content, key).decode('ascii')
	with open(file_name, "w") as myfile:
		myfile.write(decrypted_content)
	os.system("rm "+ path+"/key/"+keyname)

def str_xor(s1, s2):
	return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

# xor encryption
def xor_encryption(file_name):
	key = str(randint(1000000, 9999999))
	file_content = Path(file_name).read_text()
	multi = math.ceil(len(file_content)/len(key))
	xorKey = key*multi
	encrypted_content = str_xor(file_content, xorKey)
	with open(file_name, "w") as myfile:
		myfile.write(encrypted_content)
	return key

# xor decryption
def xor_decryption(file_name, xorKey):
	file_content = Path(file_name).read_text()
	multi = math.ceil(len(file_content)/len(xorKey))
	xorKey = xorKey*multi
	decrypted_content = str_xor(file_content, xorKey)
	with open(file_name, "w") as myfile:
		myfile.write(decrypted_content)