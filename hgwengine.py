#!/usr/bin/python

import nxppy
import time
import requests
import RPi.GPIO as GP
import json


HCL_IP = "192.168.1.10"
HCL_USER = "user"
HCL_PASS = "pass"
HCL_PIN = "1234"
HCL_ARMED_VAR = "armed"
HCL_ALARM_DEVICES = [11,15,17,21,31,44,48]
HCL_ALL_DEVICES = [5,11,15,17,19,21,31,44,48]
KNOWN_NFC_TAGS = ["3761E99E", "11FB229E", "4102E39E","F1CC67AE"] 

class Debug:
	def __init__(self,message):
		self.message = message+"\n"
	def write(self):
		file = open("/var/log/access_ctl.log","a")
		timestamp = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(time.time())))
		file.write(timestamp)
		file.write(self.message)
		file.close()
class Polling:
	def __init__(self,wuInterval,syncInterval,pollInterval):
		self.wuInterval = wuInterval
		self.syncInterval = syncInterval
		self.pollInterval = pollInterval
		self.mifare = nxppy.Mifare()
		self.arme = 0
		self.alarmDevices = HCL_ALARM_DEVICES
		self.allDevices = HCL_ALL_DEVICES
		GP.setwarnings(False)
		GP.setmode(GP.BOARD)
		GP.setup(11,GP.OUT)
		GP.output(11,False)
	
	def getUrl(self,url):
		try:
			return requests.get(url, timeout=1)
		except requests.exceptions.Timeout:
			Debug("-- Timeout for request: " + url ).write()
			return None
	


	def start(self):
		wkeup=0
		sync=0
		Debug("-- Starting Access Control").write()		
		while True:
		    try:
			if wkeup == self.wuInterval:
				for dev in self.allDevices:	
					url = "http://"+HCL_USER+":"+HCL_PASS+"@"+HCL_IP+"/api/callAction?deviceID=" + str(dev) + "&name=wakeUpDeadDevice"	
					Debug("-- Waking up device " + str(dev) + " in progress...").write()
					resp = self.getUrl(url)
					Debug("-- HCL response status: " + ( str(resp.status_code) if (resp is not None) else "None")).write()
					time.sleep(1)
				wkeup = 0
				
			
			if sync == self.syncInterval:
				url = "http://"+HCL_USER+":"+HCL_PASS+"@"+HCL_IP+"/api/globalVariables/" + HCL_ARMED_VAR
				resp = self.getUrl(url)
				if (resp and resp.ok):
					hcl_arme = int(json.loads(resp.content)['value'])
					Debug("-- HCL arming current status: " + str(hcl_arme)).write()
					if hcl_arme != self.arme:
						self.arme = hcl_arme
						Debug("-- Switching Raspi arming status to " + str(self.arme)).write()
						if self.arme == 1:
							GP.output(11,True)
						else:
							GP.output(11,False)
					sync = 0
				
			uid = self.mifare.select()
			if uid in KNOWN_NFC_TAGS :
				Debug("-- Tag from " + uid).write()
				if  self.arme == 0:
					for dev in self.alarmDevices:
						url = "http://"+HCL_USER+":"+HCL_PASS+"@"+HCL_IP+"/api/callAction?deviceID=" + str(dev) + "&name=setArmed&arg1=1"
						Debug("-- Arming device " + str(dev) + " in progress...").write()
						resp = self.getUrl(url)
						Debug("-- HCL response status: " + (str(resp.status_code) if(resp is not None) else "None")).write()
						if (resp and resp.ok):
							Debug("-- Arming device " + str(dev) + " OK").write()
						else:
							Debug("-- Arming device " + str(dev) + " KO").write()	
					url = "http://"+HCL_USER+":"+HCL_PASS+"@"+HCL_IP+"/api/sceneControl?id=4&action=start"
					Debug("-- Arming motion and entry in progress...").write()
					resp = self.getUrl(url)
					Debug("-- HCL arming response status: " + (str(resp.status_code) if(resp is not None) else "None")).write()
					if (resp and resp.ok):
						Debug("-- Arming OK").write()
						self.arme = 1
						GP.output(11,True)	
					else:
						Debug("-- Arming KO").write()
				else:
					for dev in self.alarmDevices:
						url = "http://"+HCL_USER+":"+HCL_PASS+"@"+HCL_IP+"/api/callAction?deviceID=" + str(dev) + "&name=setArmed&arg1=0&arg2=" + HCL_PIN
						Debug("-- Disarming device " + str(dev) + " in progress...").write()
						resp = self.getUrl(url)
						Debug("-- HCL response status: " + (str(resp.status_code) if(resp is not None) else "None")).write()
						if (resp and resp.ok):
							Debug("-- Disarming device " + str(dev) + " OK").write()
						else:
							Debug("-- Disarming device " + str(dev) + " KO").write()	
					GP.output(11,False)
					url = "http://"+HCL_USER+":"+HCL_PASS+"@"+HCL_IP+"/api/sceneControl?id=27&action=start"
					Debug("-- Siren OFF").write()
					resp = self.getUrl(url)
					self.arme = 0
					Debug("-- Disarming finished").write()
					
			else:
				Debug("-- Unknown tag " + (uid if uid is not None else "None")).write()
		    except nxppy.SelectError:
		        # SelectError is raised if no card is in the field.
		        pass 
		    sync += 1
		    wkeup += 1
		    time.sleep(self.pollInterval)

