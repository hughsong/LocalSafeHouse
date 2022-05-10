# SOURCE FILE:    fingerprint_client.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      TCP socket establish connection with scanner
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import socket
import sys
from random import randint
import math

# xor content with key. s1 is content, s2 is key
def str_xor(s1, s2):
	return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

# xor encryption
def xor_encryption(content, key):
	multi = math.ceil(len(content)/len(key))
	xorKey = key*multi
	encrypted_content = str_xor(content, xorKey)
	return encrypted_content

# fingerprint client socket
def finger_print_verify():
	# Server IP
	h = "192.168.1.81"
	p = 8047
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	result = []
	password = ""
	try:
		s.connect((h,p))
		password = str(randint(1000000, 9999999))
		cypher_password = xor_encryption(password, str(p))
		s.send(cypher_password.encode())

		cypher_message = s.recv(4096).decode()
		message = xor_encryption(cypher_message, password)
		if message == "match":
			return True
		else:
			return False
	except:
		return False

	return False