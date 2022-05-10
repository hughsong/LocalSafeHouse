# SOURCE FILE:    stego_photo.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      1. Used to encrypted user photo first, then the encrypted image will be hidden into a cover image 
#				  2. extract and decrypt the steganography image during face recognition
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import os, sys, time, re
import argparse
import cv2
import numpy as np
import types
from config_reader import *
from cryptography.fernet import Fernet
path = get_path()


# Description: convert string, bytes, and int to binary
def messageToBinary(message):

	if type(message) == str:
		return ''.join([format(ord(i),"08b") for i in message])
	elif type(message) == bytes or type(message) == np.ndarray:
		return [format(i,"08b") for i in message]
	elif type(message) ==int or type(message) == np.uint8:
		return format(message, "08b")
	else:
		raise TypeError("Input type not supported")


# Description: loop through image, convert all RGB to binary
def imageToBinary(image):
	binary_data = ""
	for values in image:
		for pixel in values:
			#convert the RGB values into binary format
			r,g,b = messageToBinary(pixel)
			binary_data +=r
			binary_data +=g
			binary_data +=b

	return binary_data

# Description: Randomly create a key image, and save it.
# NOTES:key image's size will be same with secret image
def generate_key_image(secret_img):
	osize = secret_img.shape
	key_name = path+"/image/.keyimg.png"
	key_img = np.random.randint(0, 256, size=(osize[0],osize[1]), dtype=np.uint8)  # Generate random key image
	cv2.imwrite(key_name, key_img)   # Save key image
	return key_name

# Description: use xor to combine key image and secret image
def encrypt(o,k):
    return np.bitwise_xor(o,k)

# Description: loop through all pixel to encrypt each RGB
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

# Description: embed encrypted secret image into cover image
def encodeData(cover_image, original_secret_image, original_secret_image_name):
	print("=====================================================")
	print("Encrypting....")
	key_name = generate_key_image(original_secret_image)
	key = cv2.imread(key_name)
	secret_image_name = "After_encryption_"+original_secret_image_name
	cv2.imwrite(secret_image_name,encryption(original_secret_image,key))
	print("Encryption finished!")
	print("=====================================================")
	print("Embedding in to cover image....")
	secret_image = cv2.imread(secret_image_name)

	name_index = 0
	data_index = 0
	counter = 0
	secret_image_name = str(secret_image.shape[0])+','+str(secret_image.shape[1])+','+original_secret_image_name+'###' # could use any string as the delimeter
	#convert input data to binary format using messageToBinary() function
	binary_secret_image_name = messageToBinary(secret_image_name)

	binary_secret_image = imageToBinary(secret_image)

	for values in cover_image:
		for pixel in values:
			counter+=1
			# convert RGB values to binary format
			r,g,b = messageToBinary(pixel)
			# modify the least significant bit only if there is still data to store
			if name_index < len(binary_secret_image_name):
				#hide the name into least significant bit of red pixel
				pixel[0] = int(r[:-1] + binary_secret_image_name[name_index], 2)
				name_index +=1
			elif data_index < len(binary_secret_image):
				#hide the data into least significant bit of red pixel
				pixel[0] = int(r[:-1] + binary_secret_image[data_index], 2)
				data_index +=1

			if name_index < len(binary_secret_image_name):
				#hide the name into least significant bit of green pixel
				pixel[1] = int(g[:-1] + binary_secret_image_name[name_index], 2)
				name_index +=1
			elif data_index < len(binary_secret_image):
				#hide the data into least significant bit of red pixel
				pixel[1] = int(g[:-1] + binary_secret_image[data_index], 2)
				data_index +=1

			if name_index < len(binary_secret_image_name):
				#hide the name into least significant bit of blue pixel
				pixel[2] = int(b[:-1] + binary_secret_image_name[name_index], 2)
				name_index +=1
			elif data_index < len(binary_secret_image):
				#hide the data into least significant bit of red pixel
				pixel[2] = int(b[:-1] + binary_secret_image[data_index], 2)
				data_index +=1

		if data_index >= len(binary_secret_image):
			break
	print("Embedding finished! ")
	print("=====================================================")
	os.system("rm After_encryption_"+original_secret_image_name)
	return cover_image, counter

# Description: extract steganographed image and decrypt it.
def decodeData(image):
	filename = ''
	counter = 0
	binary_data = ""
	image_tmp = []
	dataflag = 0
	w = 0
	h = 0
	code = get_photo_key()
	counter = int(code)
	key = cv2.imread(path+"/image/.keyimg.png")
	print("=====================================================")
	print("Decoding......")
	for values in image:
		for pixel in values:
			counter -=1
			#convert the RGB values into binary format
			r,g,b = messageToBinary(pixel)
			binary_data +=r[-1]
			binary_data +=g[-1]
			binary_data +=b[-1]
		#split by 8-bits
		all_bytes = [binary_data[i: i+8] for i in range(0,len(binary_data),8)]

		#convert from bits to characters
		decoded_data = ""
		if counter <0:
			break

	for byte in all_bytes:
		if dataflag == 0:
			decoded_data += chr(int(byte,2))
			if decoded_data[-3:] == "###":
				dataflag = 1
				filename = str(decoded_data[:-3])
		else:
			image_tmp.append(int(byte,2))

	name_list = filename.split(",")

	w = int(name_list[0])
	h = int(name_list[1])
	name = name_list[2]
	index = 0

	img= cv2.resize(image,(h,w))
	for values in img:
		for pixel in values:

			pixel[0] = image_tmp[index]
			index+=1
			pixel[1] = image_tmp[index]
			index+=1
			pixel[2] = image_tmp[index]
			index+=1

	print("Decoding finished!")
	print("=====================================================")
	print("Decrypting....")
	cv2.imwrite(path+"/image/User_org.png",encryption(img,key))
	print("Decrypting finished!")

# If cover image is not big enough to hide secret image, an exception will be raised.
def size_check(cover_image,secret_image, secret_image_name):
	#calculate the maximum bytes to encode
	n_bytes = cover_image.shape[0] * cover_image.shape[1] * 3
	#calculate how many bytes are needed to hide the secret image
	sercet_size = secret_image.shape[0] * secret_image.shape[1] * 3 * 8 + len(secret_image_name)+4+3
	if sercet_size > n_bytes:
		raise ValueError("Error encountered insufficient bytes, need bigger cover_image or less data !!")

#Description: check file name, make sure the image type is bmp or png.
def filename_check(cover_image,secret_image, steganographed_image):
	if cover_image[-3:] != "png" and cover_image[-3:] != "bmp":
		raise Exception("Only png or bmp images are accepted!")

	if cover_image[-3:] == secret_image[-3:] and cover_image[-3:] == steganographed_image[-3:]:
		pass
	else:
		raise Exception("Cover image, secret image, and steganographed image are must in same type.")

#Description: load cover image and secret image, and start encode
def load_encode_images(secret_image_name):
	st_name = 'User.png'
	cover_image_name = ".c1.png"
	print("Cover image is: ", cover_image_name)
	print("Secret image is: ", secret_image_name)
	print("steganographed image name will be: ", st_name)
	cover_image = cv2.imread(path+"/image/.c1.png")

	secret_image = cv2.imread(secret_image_name)

	tmp = secret_image_name.split("/")
	original_secret_image_name = tmp[len(tmp)-1]

	filename_check(cover_image_name, secret_image_name, st_name)

	size_check(cover_image, secret_image, secret_image_name)

	encoded_image, counter = encodeData(cover_image,secret_image,original_secret_image_name)

	cv2.imwrite(path+"/image/"+st_name,encoded_image)
	return counter

#Description: load steganographed image, and start decode
def load_decode_image():
	#read the image that contains the hidden image
	image = cv2.imread(path+"/image/User.png")
	text=decodeData(image)


