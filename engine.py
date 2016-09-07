import random

class Roll(object):

		def __init__(self):
			die1 = random.randint(1, 6)
			die2 = random.randint(1, 6)
			self._value = die1 + die2
			self._is_doubles = (die1 == die2)

		@property
		def value(self):
			return self._value
		
		@property
		def is_doubles(self):
			return self._is_doubles


class Engine(object):
	def __init__(self, num_players):
		self._state = GameState(num_players)

	def run(self):
		max_rolls = 2
		num_players = len(self._state.players)
		player = self._state.players[random.randint(0,num_players-1)]
		while not self._completed():
			roll = Roll()
			num_rolls = 0
			while roll.is_doubles:
				num_rolls += 1
				if num_rolls > max_rolls:
					self._state.apply(GroupOfChanges([GameStateChange.send_to_jail(player)]))
					break
				self._take_turn(player, roll.value)
				roll = Roll()


	def _take_turn(self, player, roll):
		position = (player.position + roll) % 40
		self._state.apply(GroupOfChanges([GameStateChange.change_position(player, position)]))
		self._state.apply(self._state.squares[position].landed(player, roll, self._state))
		self._notify_all()

	def _notify_all(self):
		changes = []
		for player in self._state.players:
			notification_changes = player.respond_to_state(self._state)
			changes.append(notification_changes)
			self._state.apply(notification_changes.other_changes)

		building_requests = [change.building_requests for change in changes]
		HousingResolver(building_requests, self._state)

	def _completed(self):
		remaining = 0
		for player in self._state.players:
			remaining += 1 if player.is_in_game

		return remaining <= 1

def main():
	engine = Engine()
	engine.run()


if __name__ == '__main__':
	main()