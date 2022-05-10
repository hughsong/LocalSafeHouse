# SOURCE FILE:    file_modification.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      bridge between the front-end UI and the back-end database.
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
from SQL_database import *
from file_encryption import *
import shutil

connection = make_connection()

# generate and verify TOTP
# Prepare the email content and send out 2-step verification email
def two_factor_verification(filename):
	encrypt_order = get_encrypt_order(connection,filename)
	encrypt_keys = get_encrypt_keys(connection,filename,encrypt_order)
	EMAIL_ADDRESS = "HughSong0107@gmail.com"
	msg = EmailMessage()
	msg['Subject'] = "safehouse 2 step verification"
	msg['From'] = EMAIL_ADDRESS
	msg['To'] = "hugh.happy.everyday@gmail.com"
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret, interval=90)

	with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
		smtp.login("HughSong0107@gmail.com", "96990107syh")
		secret = pyotp.random_base32()
		token = totp.now()
		# sender, receiver
		msg.set_content("Securty key: "+str(token)+"\nEncryption order: "+encrypt_order+"\nKeys: "+encrypt_keys)
		smtp.send_message(msg)
	return totp

# Copy the file into level folder; 
# Insert file information into database
def add_file(file_path,level_path,level):
	path = get_path()
	path = os.path.join(path,level_path)
	shutil.copy(file_path, path)
	tmp = file_path.split("/")
	name = tmp[len(tmp)-1]
	insert_file_db(connection,name,level)

# determine which method the user want to use, then call the corresponding encryption method
# update database to enter the encryption information
def encrypt_file(name,method,level_path):
	path = get_path()
	path = os.path.join(path,level_path)
	file_path = os.path.join(path,name)
	key = ""
	if method == "cryptography":
		key = cryptography_encrypt(file_path)
	elif method == "aesEncrypt":
		key = aes_encrypt(file_path)
		os.system("rm "+ file_path)
	elif method == "xorEncrypt":
		key = xor_encryption(file_path)
	elif method == "rsaEncrypt":
		key = rsa_encrypt(file_path)
	encrypt_file_db(connection,name, method, key)

# remove file from folder, delete record from db
def delete_file(name,level_path):
	path = get_path()
	path = os.path.join(path,level_path)
	file_path = os.path.join(path,name)
	delete_file_db(connection,name)
	os.system("rm "+ file_path)

# using commands to open the file
def edit_file(name,level_path):
	path = get_path()
	path = os.path.join(path,level_path)
	file_path = os.path.join(path,name)
	os.system("open "+ file_path)

# use input decryption order to decrypt the file layer by layer
# update database to remove the previous encryption information
def decrypt_file(level_path,name,decrypt_order,decrypt_key):
	path = get_path()
	path = os.path.join(path,level_path)
	file_path = os.path.join(path,name)
	if not decrypt_order_validation(connection, name, decrypt_order):
		return False
	decrypt_order_list = decrypt_order.split(" ")
	decrypt_key_list = decrypt_key.split(" ")
	try:
		for i in range(0, len(decrypt_order_list)):
			if decrypt_order_list[i] == "cryptography":
				cryptography_decrypt(file_path,decrypt_key_list[i])
			elif decrypt_order_list[i] == "aesEncrypt":
				aes_decrypt(file_path, decrypt_key_list[i])
				os.system("rm "+ file_path+".aes")
				#os.system("rm "+ file_path)
			elif decrypt_order_list[i] == "xorEncrypt":
				xor_decryption(file_path, decrypt_key_list[i])
			elif decrypt_order_list[i] == "rsaEncrypt":
				rsa_decrypt(file_path, decrypt_key_list[i])

			decrypt_file_db(connection,name, decrypt_order_list[i])
	except:
		return False
	return True

# get existing files in this level
def show_all_files(level):
	unencrypted_files_list, encrypted_files_list = get_file_names(connection,level)
	return unencrypted_files_list, encrypted_files_list
