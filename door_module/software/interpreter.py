from logging import warn

class Interpreter:
	def __init__(self, opener, beeper_outside,beeper_inside):
		self.opener=opener
		self.beeper_inside=beeper_inside
		self.beeper_outside=beeper_outside

	def do(self,command):
		if command['type']=='open':
			self.opener()
		elif command['type']=='beep':
			style=command['beepstyle']
			if command['location']=='inside':
				beeper_inside(style)
			elif command['location']=='outside':
				beeper_outside(style)
			else:
				beeper_inside(style)
				beeper_outside(style)
