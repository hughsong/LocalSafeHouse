# SOURCE FILE:    folder_maze.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      Create folder maze, application folders and path. 
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import os
import shutil
from config_reader import *

print("[+]Start creating folder maze...")
app_name = get_app_name()
root_path=os.path.expanduser('~')
user_dir = os.path.join(root_path,app_name)
#create folder maze
os.mkdir(user_dir)
for i in range(1,11):
	path1=os.path.join(user_dir,str(i))
	os.mkdir(path1)
	for j in range(1,11):
		path2=os.path.join(path1,str(j))
		os.mkdir(path2)
		for k in range(1,11):
			path3=os.path.join(path2,str(k))
			os.mkdir(path3)
			for n in range(1,11):
				path4=os.path.join(path3,str(n))
				os.mkdir(path4)

# PIN is the correct file path
PIN = get_PIN()
# record correct program path
destination_path = user_dir
for i in PIN:
	destination_path=os.path.join(destination_path,i)
# encrypt PIN
set_PIN(str(int(PIN)*222))
# create a image folder under the correct program path and upload user image
image_path = os.path.join(destination_path,"image")
os.mkdir(image_path)
shutil.copy(".c1.png", image_path)
# create a image folder under the correct program path and upload user image
key_folder_path = os.path.join(destination_path,"key")
os.mkdir(key_folder_path)

#create level 1 folder;
level_1 = os.path.join(destination_path,"level1")
os.mkdir(level_1)
#create level 2 folder;
level_2 = os.path.join(level_1,"level2")
os.mkdir(level_2)
#create level 3 folder;
level_3 = os.path.join(level_2,"level3")
os.mkdir(level_3)
print("[+]Folder maze has been created!")