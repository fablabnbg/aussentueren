class StatusManager:
	def __init__(self,on_change):
		self.on_change=on_change
		self._open=False
		self._public=False
		self._occupied=False

	def publish(self):
		self.on_change(self)

	@property
	def status(self):
		if not self.open:
			return 'locked'
		if self.public:
			return 'public'
		return 'unlocked'

	@property
	def open(self):
		return self._open

	@open.setter
	def open(self,status):
		if self._open!=status:
			self._open=status
			self.on_change(self)

	@property
	def occupied(self):
		return self._occupied

	@occupied.setter
	def occupied(self,status):
		if self._occupied!=status:
			self._occupied=status
			self.on_change(self)

	@property
	def public(self):
		return self._public

	@public.setter
	def public(self,status):
		if not self.occupied:
			return
		if self._public!=status:
			self._public=status
			self.on_change(self)
