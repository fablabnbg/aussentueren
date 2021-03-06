from datetime import datetime
from parameters import max_delay_card_pin_seconds

class Identity_store:
	def __init__(self):
		self._uid=None
		self._sak=None
		self._last_time=datetime.now()
	
	@property
	def uid(self):
		if (datetime.now()-self._last_time).seconds>max_delay_card_pin_seconds:
			self._uid=None
		return self._uid

	@uid.setter
	def uid(self,new_uid):
		self._uid=new_uid
		self._last_time=datetime.now()

	@property
	def sak(self):
		if (datetime.now()-self._last_time).seconds>max_delay_card_pin_seconds:
			self._sak=None
		return self._sak

	@sak.setter
	def sak(self,new_sak):
		self._sak=new_sak
