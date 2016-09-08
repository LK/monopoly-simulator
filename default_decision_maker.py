class DefaultDecisionMaker(object):
	def __init__(self):
		pass

	def _can_mortgage_property(prop, state):
		for prop in state.get_property_group(prop.property_group):
			if prop.num_houses > 0:
				return False

		return True

	def _demolish_from_property_group(prop, state):
		max_houses = 0
		max_houses_prop = None
		for prop in state.get_property_group(prop.property_group):
			if prop.num_houses > max_houses:
				max_houses = prop.num_houses
				max_houses_prop = prop

		if max_houses_prop != None:
			return GameStateChange.demolish(max_houses_prop, state.bank)
		else:
			return None

	def buy_or_deny(player, prop, state):
		if player.cash >= prop.price:
			return GroupOfChanges(changes=[GameStateChange.transfer_money(state.bank, player, prop.price)])
		else:
			return GroupOfChanges(changes=[])

	def pay(player_from, player_to, amount, state):
		changes = [GameStateChange.transfer_money(player_from, player_to, amount)]
		difference = amount - player.cash
		while difference > 0:
			for prop in player_from.props:
				if not prop.mortgaged and _can_mortgage_property(prop, state):
					changes.append(GameStateChange.mortgage(prop, state.bank))
					continue

			for prop in player_from.props:
				if prop.num_houses > 0:
					changes.append(_demolish_from_property_group(prop, state))
					continue

			return GroupOfChanges(changes=[GameStateChange.eliminate(player_from, player_to)])

		return GroupOfChanges(changes=changes)

	def bid_house_builds(player, highest_bid, props_to_build_on):
		pass

	def bid_hotel_builds(player, highest_bid, props_to_build_on):
		pass