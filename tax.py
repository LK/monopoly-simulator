from square import Square

class Tax(Square):

	def __init__(self, tax):
		self._tax = tax

	def landed(self, player, state):
		return player.pay(Square.BANK, self._tax, state)