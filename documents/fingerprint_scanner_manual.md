# Fingerprint scanner server installation manual
## Required Hardware
 - Raspberry PI 4 with Debian operating system
 - Adafruit Optical Fingerprint Sensor
 - A female-to-female jumper wire

## Hardware Setup
Before wiring, user should disable the console to use built in UART on the RX/TX pins.

Run command “sudo raspi-config” and select the following:
![scanner_setup1](/img/scanner_setup1.png)
![scanner_setup2](/img/scanner_setup2.png)

Then reboot.  
Once you've rebooted, you can use the built in UART via /dev/ttyS0.  
Wire the GPS as follows:  
Plug one side of the jumper wire into fingerprint sensor  
![scanner_wiring](/img/scanner_wiring.png)

Plug another side into Raspberry PI board.  
Raspberry PI Pinout Image:  
In this case, we will use:  
![scanner_wiring](/img/PI_pinout.png)

After the fingerprint sensor correctly connected with Raspberry PI, you will see the green light on the sensor when you turn on Raspberry PI.
![scanner_connected](/img/scanner_connected.png)

## Software Setup
 1. Once the hardware part done, from your command line run the following command: sudo pip3 install adafruit-circuitpython-fingerprint
 2. Manually set your PI’s IPV4 address to be 192.168.1.81
 3. Running the script fingerprint_scanner.py to start the server: python3 fingerprint_scanner.py
