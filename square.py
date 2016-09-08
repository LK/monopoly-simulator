class Square(object):
	# Methods

	def __init__(self, name):
		self._name = name

	def landed(self, player, roll, state):
		raise NotImplementedError("landed() called from an instance of Square")

	@property
	def name(self):
		return self._name

	def __str__(self):
		s = "Name: %s\n" % (self._name)
		return s