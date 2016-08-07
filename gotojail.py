from square import Square

class GoToJail(Square):

	JAIL_MOVES = 3

	def landed(self, player, state):
		return GameStateChange(new_position={ player : Square.INDEX["jail"] },
			change_in_jail_moves={ player : JAIL_MOVES })