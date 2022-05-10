import os, sys, time, re
import cv2
import numpy as np
import types
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
path = config['folde_maze']['destination_path']
#-----------------------------------------------------------------
#FUNCTION generate_key_image
#ARGUMENTS: cv2 object, string
#RETURNS: string
#Description: Randomly create a key image, and save it.
#NOTES:
#key image's size will be same with secret image
#-----------------------------------------------------------------
def generate_key_image(secret_img):
	osize = secret_img.shape
	key_name = path+"/image/.userKey.png"

	key_img = np.random.randint(0, 256, size=(osize[0],osize[1]), dtype=np.uint8)  # Generate random key image
	cv2.imwrite(key_name, key_img)   # Save key image
	return key_name

#-----------------------------------------------------------------
#FUNCTION encrypt
#ARGUMENTS: bytes, bytes
#RETURNS: bytes
#Description: use xor to combine key image and secret image
#-----------------------------------------------------------------
def encrypt(o,k):
    return np.bitwise_xor(o,k)

#-----------------------------------------------------------------
#FUNCTION encryption
#ARGUMENTS: cv2 object, cv2 object
#RETURNS: ndarray
#Description: loop through all pixel to encrypt each RGB
#-----------------------------------------------------------------
def encryption(secret_img, key_img):
	obgr = cv2.split(secret_img)
	kbgr = cv2.split(key_img)
	cbgr = []
	#encrypt each RGB
	for i,v in enumerate(obgr):
		t=encrypt(v,kbgr[i])
		cbgr.append(t)

	c = cv2.merge(cbgr)
	return c

def encryptPhoto(original_secret_image):
	print("=====================================================")
	print("Encrypting user photo....")
	key_name = generate_key_image(original_secret_image)
	key = cv2.imread(key_name)
	secret_image_name = path+"/image/User1.png"
	cv2.imwrite(secret_image_name,encryption(original_secret_image,key))
	print("Encryption finished!")