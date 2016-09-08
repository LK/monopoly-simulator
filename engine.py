from random import randint
from gamestate import GameState
from roll import Roll
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from constants import *

class Engine(object):
	def __init__(self, num_players):
		self._state = GameState(num_players)

	def run(self):
		max_rolls = 2
		num_players = len(self._state.players)
		player = self._state.players[randint(0,num_players-1)]
		while not self._completed():
			roll = Roll()
			if player.jail_moves > 0 and roll.is_doubles:
				self._state.apply(GroupOfChanges(changes=[GameStateChange.leave_jail(player)]))
			elif player.jail_moves >= 2:
				self._state.apply(GroupOfChanges(changes=[GameStateChange.decrement_in_jail_moves(player)]))
			elif player.jail_moves == 1:
				pay_changes = player.pay(state.bank, 50, self._state)
				leave_changes = GroupOfChanges(changes=[GameStateChange.leave_jail(player)])
				self._state.apply(GroupOfChanges.combine([pay_changes, leave_changes]))

			num_rolls = 0
			while roll.is_doubles:
				num_rolls += 1
				if num_rolls > max_rolls:
					self._state.apply(GroupOfChanges(changes=[GameStateChange.send_to_jail(player)]))
					break
				self._take_turn(player, roll.value)

				roll = Roll()


	def _take_turn(self, player, roll):
		position = (player.position + roll) % NUM_SQUARES
		self._state.apply(GroupOfChanges([GameStateChange.change_position(player, position)]))
		self._state.apply(self._state.squares[position].landed(player, roll, self._state))
		self._notify_all()

		cmd = raw_input('')
		if cmd == 'state':
			print str(self._state)

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
			 if player.is_in_game:
			 	remaining += 1

		return remaining <= 1

def main():
	engine = Engine(4)
	engine.run()


if __name__ == '__main__':
	main()