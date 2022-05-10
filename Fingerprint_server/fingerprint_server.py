# SOURCE FILE:    fingerprint_server.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      TCP server socket establish connection with client
#                 Three modes: print registration, server, and print deletion.
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import socket
from fingeprint_verify import *
import time, os, sys
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

# server mode (TCP server socket)
def server_socket():
    host = ''
    port = 8047
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    while 1:
        s.listen(1)
        print('Waiting for connection')
        #-------control channel connection--------
        conn, addr = s.accept()
        print('Got connection from: ', addr)
        key = conn.recv(4096).decode()
        content = xor_encryption(key, str(port))
        match_result=False
        counter = 0
        while counter<3:
            print("----------------")
            if finger.read_templates() != adafruit_fingerprint.OK:
                raise RuntimeError("Failed to read templates")
            if get_fingerprint():
                print("Detected #", finger.finger_id, "with confidence", finger.confidence)
                match_result = True
                break
            else:
                print("Finger not found, please try again!")
                counter+=1
            if counter == 3:
                print("You fail the finger print validation!")
                break
        print("-------Verification End---------")
        if match_result:
            message = "match"
            cypher_message = xor_encryption(message,content)
            conn.send(cypher_message.encode())
        else:
            message = "failed"
            cypher_message = xor_encryption(message,content)
            conn.send(cypher_message.encode())
            cmd = "iptables -A INPUT -p tcp --dport 8047 -j REJECT"
            os.system(cmd)
            time.sleep(90)
            cmd = "iptables -D INPUT -p tcp --dport 8047 -j REJECT"
            os.system(cmd)
        conn.close()

if __name__ == "__main__":
    print("Welcome for using LocalSafeHouse fingerprint scanner!")
    print("     >>Press '1' to register your finger.")
    print("     >>Press '2' to start the server.")
    print("     >>Press '3' to delete print from server.")
    choice = input("Choice: ")
    if choice == "2":
        server_socket()
    elif choice == "1":
        enroll_finger(get_num())
    elif choice == "3":
        if finger.delete_model(get_num()) == adafruit_fingerprint.OK:
           print("Deleted!")
        else:
           print("Failed to delete")

