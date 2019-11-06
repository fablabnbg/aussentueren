"""The IOctrl module enables access to the integrated peripherals of 
the Arietta G25.

IOctrl.gpio : read or write gpio pins
IOctrl.adc  : read ADC (not implemented)
"""

import time
import threading
import os
import select

class gpio:
	"""The gpio class represents one gpio pin.

	gpio(num,direction=None)
	num : number of the controlled pin
	direction : 'in' or 'out'
	"""
	def __init__(self,num,direction=None,active_low=False):
		self.tap_active=False
		self.devname='/sys/class/gpio/gpio'+str(num)
		if not os.path.exists(self.devname):
			with open('/sys/class/gpio/export','w') as f:
				f.write(str(num))
		time.sleep(0.5)

		with open(os.path.join(self.devname,'active_low'),'w') as f:
			f.write(str(int(active_low)))

		if direction:
			self.set_dir(direction)

	def set_dir(self,direction):
		"""Set direction of pin.
		Either 'in' or 'out'
		"""
		if not direction in ('in','out'):
			raise ValueError('direction must be "in" or "out" not "{}"'.format(direction))
		self.direction=direction
		with open(os.path.join(self.devname,'direction'),'w') as f:
			f.write(self.direction)
			time.sleep(0.1)

	def set_interrupt(self,int_type):
		"""Set edge on which 'wait' will return.
		Can be 'rising', 'falling' or 'both'
		"""
		if not int_type in ('rising','falling','both'):
			raise ValueError('int_type must be "rising", "falling" or "both" not "{}"'.format(int_type))
		with open(os.path.join(self.devname,'edge'),'w') as f:
			f.write(int_type)

	def set(self,value,change=False):
		"""Set value on pin to high (1) or low (0).
		set(value,change=False)
		value : either 1 or 0
		change : set to one to automatically change direction to 'out'
		"""
		if self.tap_active:
			return

		if not self.direction=='out':
			if change:
				self.direction('out')
			else:
				raise ValueError('Port is set to input and function not asked to change')
		if not value in (0,1):
			raise ValueError('Can only set value to one or zero not "{}"'.format(value))
		with open(os.path.join(self.devname,'value'),'w') as f:
			f.write(str(value))

	def tap(self,duration):
		"""Set value to high for duration and low again afterwards.

		tap(duration)
		duration : time in seconds to keep pin high
		"""
		def runthread():
			self.set(1)
			self.tap_active=True
			time.sleep(duration)
			self.tap_active=False
			self.set(0)
		threading.Thread(target=runthread).start()

	def get(self,change=False):
		"""Get current value on pin. Returns 1 or 0.
		get(change=False)
		change : set to True to automatically change direction to 'in'
		"""
		if not self.direction=='in':
			if change:
				self.direction('in')
			else:
				raise ValueError('Port is set to output and function not asked to change')
		with open(os.path.join(self.devname,'value'),'r') as f:
			return int(f.read())
	
	def wait(self):
		"""For for edge defined with 'set_interrupt'"""
		p=select.poll()
		with open(os.path.join(self.devname,'value')) as f:
			f.read()
			p.register(f,select.POLLPRI|select.POLLERR)
			p.poll()

class adc:
	def __init__(self,num):

		pass
