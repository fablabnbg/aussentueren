class StatusManager:
	def __init__(self,on_change):
		self.on_change=on_change
		self._open=False
		self._public=False

	@property
	def status(self):
		if not self.open:
			return 'closed'
		if self.public:
			return 'public'
		return 'open'

	@property
	def open(self):
		return self._open

	@open.setter
	def open(self,status):
		if self._open!=status:
			self._open=status
			self.on_change(self.status)

	@property
	def public(self):
		return self._public

	@public.setter
	def public(self,status):
		print(status)
		if not self.open:
			return
		if self._public!=status:
			self._public=status
			self.on_change(self.status)
