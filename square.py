class Square(object):
	
	# Constants
	INDEX = { }			# dictionary maps names to indices
	BANK = None			# represents the bank

	# Import square names
	SQUARE_NAMES_FILE = "squares.txt"
	f = open(SQUARE_NAMES_FILE, "r")
	i = 0
	for line in f:
		INDEX[line[:-1]] = i
		i += 1

	def __init__(self, name):
		self._name = name

	def landed(self, player, roll, state):
		raise Exception("Subclass did not implement landed()")

	@property
	def name(self):
		return self._name
	