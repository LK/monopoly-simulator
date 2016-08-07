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

	def landed(self, player, state):
		raise Exception("Subclass did not implement landed()")