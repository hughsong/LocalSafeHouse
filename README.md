# LocalSafeHouse

## Project Description
The Localsafehouse project described in is a Linux application. The goal of this project is to protect personal and sensitive files locally. Instead of just uploading and saving files into cloud platforms or third-party servers, this project mainly focuses on using novel verification methods include face recognition and fingerprint, and two-factor authentication to protect local files. According to the files’ importance level, each level has its corresponding verification. Some crucial files could be encrypted many times by using several encryption methods. In addition, the two-factor authentication technique is used together with encryption techniques; as a result, crucial files only could be opened when the user has one time security key, correct encryption order and correct decryption keys, which are sent by email to users.

## Project Structure
The program has three different layers to store files; they are named “level1”, “level2”, and “level3”. level1 stores the less important fires, and level3 stores the most important files. Each level has its corresponding verification method.
### Macro Structure
![Macro structure](/img/macro-structure.png)
### Network Diagram
![Network diagram](/img/network_diagram.png)

## Statement Flow Diagram
There will be three flow charts in this section. The first chart is the flow chart for passing verifications. It shows the user registration phase, password verification from the login page to level1 page, face recognition from level1 page to level2 page, client-side view of fingerprint verification from level2 page to level3 page. The second chart shows the flow chart for file processing on each level. It is a part of the first chart. I separate it because the chart will look very disorderly if I put them all together. It contains 'add', 'encrypt', 'decrypt', 'delete', and 'edit' functions. The third chart shows the flow chart for the fingerprint scanner server.

[Flow chart for verifications (client side)](/documents/fc_verifications.md)

[Flow chart for file processing (client side)](/documents/fc_file_process.md)

[Flow chart for fingerprint scanner server (scanner side)](/documents/fc_fingerprint.md)

## User Manual
### 1. Fingerprint Scanner Setup:
Please follow my [fingerprint scanner installation manual](/documents/fc_verifications.md) to make the server ready.
Register user fingerprint on the scanner:
 - execute scanner script: python3 fingerprint_scanner.py
 - Press ‘1’ to register fingerprint
 - follow the steps showed on the terminal

After fingerprint registration, execute scanner script again and press ‘2’ to start the server.

### 2. Client Side Software Setup:
 - Users need to make sure python3 is already installed on the device. Using command “python3 –version” to check your python version.
 - Users need to execute source file “setup.sh” with the command “./setup.sh” to install all necessary python libraries. (If some packets are still missing, please flow the error message to install them manually.)
 - Users need to install MYSQL database from their official website. (There is no installation and setup instruction for MYSQL database in this report because it is out of scope).
 - After the MYSQL database is set up, use a text editor to open the source file “SQL_database.py” and replace line#19 with your database password. Then, the user needs to uncomment line#190 and line#191 and execute it with the command “python3 SQL_database.py” to create the database table for the application. After the table is created, please comment out line#190 and line#191.
 - Users need to execute source file “set_up.py” with command “python3 set_up.py” to initial the configuration file.
 - Users need to execute source file “folder_maze.py” with command “python3 folder_maze.py” to setup the application folder.

### 3. User Registration:
 - Running the application with command “python3 LocalSafeHouse.py”
 - Click on “Register” button

 ![register btn](/img/register_btn.png)

 - Enter your information into the registration form. (Email address must be a Gmail) 
 - Click on the “Upload Photo” button to upload the user photo. (The photo must contain the user’s entire face without any cover. The image must be a png or BMP file, the image height*width should be smaller than 300\*400)

  ![upload photo](/img/upload_photo.png)
 - Click on “submit” button.

## Functionality
 - Login function (Entering level1 folder)
 - Enter level 2 folder (Face recognition)
 - Enter level 3 folder (Fingerprint verification)
 - File operations (upload/view/edit/delete)
 - File encryption/decryption 
 (Detail of the above functionalities)

 &nbsp;&nbsp;&nbsp;&nbsp;[(Detail of the above functionalities)](/documents/functionalities.md)

# Library References
 - UI: tkinter
 - Image: face_recognition;  cv2;  numpy
 - File encrypt/decrypt: RSA;  AES;  fernet;  pyotp
 - Database: pandas; mysql-connector-python;  


## Project Demo
Demo video please check from my youtube channel:
https://youtu.be/pff6eK6UvQM

