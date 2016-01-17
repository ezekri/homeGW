# homeGW
Raspi home automation GateWay

# Description 
Control Fibaro Home Center Lite (HCL) security devices with NXP-Explorer NFC controller 


# Dependencies
RPi.GPIO : Rapsi GPIO library, by default installed in Raspbian

nxppy : NXP-Explorer library (https://github.com/svvitale/nxppy)


# Install
git clone https://github.com/ezekri/homeGW.git

# Configure global variables

HCL_IP = Fibaro Home center IP address

HCL_USER = Home Center user name

HCL_PASS = Home center password

HCL_PIN = Home center disarming pin code

HCL_ARMED_VAR = global variable defined in HCL for arming status  

HCL_ALARM_DEVICES = list of alarm devices

HCL_ALL_DEVICES = list of all devices

KNOWN_NFC_TAGS = list of nfc tags permitted to control alarm 

# Configure startup service
sudo cp homegw /etc/init.d/

chmod 755 /etc/init.d/homegw

update-rc.d homegw defaults

# start/stop/status homegw
sudo service homegw start

sudo service homegw stop

sudo service homegw status
