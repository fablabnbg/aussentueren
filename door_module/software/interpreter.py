from logging import warn

class Interpreter:
	def __init__(self, opener, public, beeper_outside,beeper_inside):
		self.opener=opener
		self.public=public
		self.beeper_inside=beeper_inside
		self.beeper_outside=beeper_outside

	def do(self,command):
		if command['type']=='open':
			self.opener()
		elif command['type']=='close':
			self.public(False)
		elif command['type']=='beep':
			style=command['beepstyle']
			if command['location']=='inside':
				self.beeper_inside(style)
			elif command['location']=='outside':
				self.beeper_outside(style)
			else:
				self.beeper_inside(style)
				self.beeper_outside(style)

	def do_status(self,status):
		self.public(status==b"public")


