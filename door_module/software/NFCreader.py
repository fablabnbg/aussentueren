import threading
import serial
import time
import logging
from datetime import datetime

class NFCreader_stub:
    def __init__(self,*args,**kwargs):
        pass
    def run(self):
        pass
    def beep(self, a):
        pass
    def start(self,*args,**kwargs):
        pass

class NFCreader(threading.Thread):
	"""The NFCreader class controls an NFC reader on a serial port.
	To actually start communication the "start"-method has to be called.

	NFCreader(dev, on_card)
	dev : path to serial device
	on_card : callback executed when the reader signals a new card
	"""

	def __init__(self,dev,on_card,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.callback=on_card
		self.s=serial.Serial(dev,9600,timeout=0)
		self.beepcmd=b''
		self.last_uid=None
		self.last_time=datetime.now()

	def run(self):
		"""Executed on new thread by "start"."""
		while True:
			if self.beepcmd:
				self.s.write(self.beepcmd)
				self.beepcmd=b''
			line=self.s.readline()
			if line:
				self._interpret(line)
			else:
				time.sleep(0.1)

	def beep(self,beepcmd):
		"""Instruct NFCreader to play the given tune
		"""
		self.beepcmd=beepcmd

	def _interpret(self,line):
		try:
			if not line.startswith(b'#'):
				lineparts=line.strip().split(b' ')
				sak,uid,chk=lineparts
				uid_bytes=bytes.fromhex(uid.decode('utf8'))
				sak_int=int(sak,16)
				sum_uid=sum(uid_bytes)
				chk_int=int(chk,16)
				checksum=(sak_int+sum_uid)&0xff
				if checksum!=int(chk,16):
					logging.warn("Checksum Error for card {} {} {}. expected {}".format(sak,uid,chk,hex(checksum)))
					return
				now=datetime.now()
				if (now-self.last_time).seconds<0.5: # Ratelimit NFC Cards to max 2 per second
					return
				if (datetime.now()-self.last_time).seconds>2: # Accept same card again after 2 seconds
					self.last_uid=None
				if uid==self.last_uid: #ignore repeated reads of the same card
					return
				self.last_uid=uid
				self.last_time=datetime.now()
				self.callback(uid,sak)
		except Exception as e:
			pass
