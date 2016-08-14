from square import Square
from gamestatechange import GameStateChange

class GoToJail(Square):

	JAIL_MOVES = 3

	def landed(self, player, roll, state):
		return GameStateChange(new_position={ player: Square.INDEX["jail"] },
			change_in_jail_moves={ player: JAIL_MOVES })