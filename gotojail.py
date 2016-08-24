from square import Square
from gamestatechange import GameStateChange

class GoToJail(Square):

	JAIL_MOVES = 3

	def __init__(self, name):
		super(GoToJail, self).__init__(name)

	def landed(self, player, roll, state):
		return GameStateChange(new_position={ player: Square.INDEX["jail"] },
			change_in_jail_moves={ player: JAIL_MOVES })