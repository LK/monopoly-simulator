import random

class Engine(object):
	def __init__(self, num_players):
		self.num_players = num_players
		self.state = GameState(num_players)

	def run(self):
		player = self.state.players[random.randint(0,self.num_players-1)]
		while not self.completed():
			self.take_turn(player)

	@staticmethod
	def roll():
			return random.randint(1,6) + random.randint(1,6)

	def take_turn(self, player):
		dice = Engine.roll()
		position = (player.position + dice) % 40
		
		if player.position + dice >= 40:
			self.state.apply(GameStateChange(new_position={player: position}, change_in_cash={player: 200}))
		else:
			self.state.apply(GameStateChange(new_position={player: position}))

		self.notify_all()
		self.state.apply(self.state.squares[position].landed(player, self.state))
		self.notify_all()

	def notify_all(self):
		changes = []
		for player in self.state.players:
			goc = player.notify(self.state)
			changes.append(goc)
			self.state.apply(goc.other_changes)

		

		if self.state.are_enough_houses(total_houses):
			for change in changes:
				self.state.apply(goc.building_changes)
		else:
			for i in range(self.state.houses_remaining):
				self.auction()

	def auction(self):
		

	def completed(self):
		remaining = 0
		for player in self.state.players:
			remaining += 1 if player.is_in_game

		return remaining <= 1

def main():
	engine = Engine()
	while not engine.completed(state):


if __name__ == '__main__':
	main()