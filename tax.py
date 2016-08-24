from square import Square

class Tax(Square):

	def __init__(self, name, tax):
		super(Tax, self).__init__(name)
		self._tax = tax

	def landed(self, player, roll, state):
		return player.pay(Square.BANK, self._tax, state)