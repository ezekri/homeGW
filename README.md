# homeGW
Raspi home automation GateWay

# Description 
Control Fibaro Home Center Lite (HCL) security devices with NXP-Explorer NFC controller 


# Dependencies
RPi.GPIO : Rapsi GPIO library, by default installed in Raspbian

nxppy : NXP-Explorer library (https://github.com/svvitale/nxppy)


# Install
git clone https://github.com/ezekri/homeGW.git


# Configure startup service
sudo cp homegw /etc/init.d/
chmod 755 /etc/init.d/homegw
update-rc.d homegw defaults

# start/stop/status homegw
sudo service homegw start
sudo service homegw stop
sudo service homegw status
