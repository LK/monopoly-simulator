from square import Square
from deck import Deck
from gamestatechange import GameStateChange
from gamestate import GameState
from gotojail import GoToJail
from sys import argv

class Card(Square):

	# Constants
	CHANCE_CARD = True
	COMMUNITY_CHEST_CARD = not CHANCE_CARD
	CHANCE_PER_HOUSE_FEE = 25
	CHANCE_PER_HOTEL_FEE = 100
	COMMUNITY_CHEST_PER_HOUSE_FEE = 40
	COMMUNITY_CHEST_PER_HOTEL_FEE = 115

	# Chance and community chest functions
	@staticmethod
	def _advance_to_square(player, state, square_name):
		return GameStateChange(new_position={ player: Square.INDEX[square_name] })

	@staticmethod
	def _advance_to_go(player, state):
		return _advance_to_square(player, state, "go")

	@staticmethod
	def _go_to_jail(player, state):
		return GameStateChange(new_position={ player: Square.INDEX["jail"] },
			chance_in_jail_moves={ player : GoToJail.JAIL_MOVES })

	@staticmethod
	def _pay_building_fees(player, state, per_house_fee, per_hotel_fee):
		total_houses = 0
		total_hotels = 0
		for prop in player.props:
			if isinstance(prop, ColorProperty):
				if prop.has_hotel():	# TODO: ColorProperty needs to implement has_hotel()
					total_hotels += 1
				else:
					total_houses += prop.num_houses()
		fee = (total_houses * per_house_fee) + (total_hotels * per_hotel_fee)
		return player.pay(Square.BANK, fee, state)

	@staticmethod
	def _collect(player, state, amount):
		return GameStateChange(change_in_cash={ player: amount })

	@staticmethod
	# TODO: Need to remove "get out of jail free" from the deck while a player has it
	def _get_out_of_jail_free(player, state):
		return GameStateChange(change_in_jail_free_count={ player: +1 })



	# Chance-only functions
	@staticmethod
	def _collect_50(player, state):
		return _collect(player, state, 50)

	@staticmethod
	def _collect_150(player, state):
		return _collect(player, state, 150)

	@staticmethod
	def _pay_each_player_50(player, state):
		changes_paying_players = []
		for other_player in state.players:
			if other_player != player:
				changes_paying_players.append(player.pay(other_player, 50, state))
		all_payments = GameStateChange.combine(changes_paying_players)
		return all_payments

	@staticmethod
	def _pay_poor_tax_of_15(player, state):
		return player.pay(player, 15, state)

	@staticmethod
	def _pay_building_fees_chance(player, state):
		return _pay_building_fees(player, state, CHANCE_PER_HOUSE_FEE,
			CHANCE_PER_HOTEL_FEE)

	# Helper function for "advance to nearest __________" cards.
	# Returns the square nearest to the given position going forward
	@staticmethod
	def _nearest_to(position, square_indices):
		min_dist = GameState.NUM_SQUARES + 1
		nearest = square_indices[0]
		for square_index in square_indices:
			if square_index - position < 0:
				# Account for going around the board mod 40
				dist_to_go = -position % GameState.NUM_SQUARES
				dist = dist_to_go + square_index
			else:
				dist = square_index - position

			if dist < min_dist:
				min_dist = dist
				nearest = square_index
		return nearest

	@staticmethod
	def _advance_to_nearest_utility(player, state):
		electric_company 	= Square.INDEX["electric_company"]
		water_works 			= Square.INDEX["water_works"]
		nearest_utility 	= nearest_to(player.position, [electric_company,
			water_works])
		return GameStateChange(new_position={ player: nearest_utility })

	@staticmethod
	def _advance_to_nearest_railroad(player, state):
		reading_railroad 			= Square.INDEX["reading_railroad"]
		pennsylvania_railroad	= Square.INDEX["pennsylvania_railroad"]
		b_and_o_railroad 			= Square.INDEX["b_and_o_railroad"]
		short_line_railroad 	= Square.INDEX["short_line_railroad"]
		nearest_railroad 			= nearest_to(player.position, [reading_railroad,
			pennsylvania_railroad, b_and_o_railroad, short_line_railroad])
		return GameStateChange(new_position={ player: nearest_railroad })

	@staticmethod
	def _advance_to_reading_railroad(player, state):
		return _advance_to_square(player, state, "reading_railroad")

	@staticmethod
	def _advance_to_boardwalk(player, state):
		return _advance_to_square(player, state, "boardwalk")

	@staticmethod
	def _advance_to_illinois_avenue(player, state):
		return _advance_to_square(player, state, "illinois_avenue")

	@staticmethod
	def _advance_to_st_charles_place(player, state):
		return _advance_to_square(player, state, "st_charles_place")

	@staticmethod
	def _go_back_three_spaces(player, state):
		return GameStateChange(new_position={ player: player.position - 3 })




	# Community-chest-only functions
	@staticmethod
	def _collect_10(player, state):
		return _collect(player, state, 10)

	@staticmethod
	def _collect_20(player, state):
		return _collect(player, state, 20)

	@staticmethod
	def _collect_25(player, state):
		return _collect(player, state, 25)

	@staticmethod
	def _collect_45(player, state):
		return _collect(player, state, 45)

	@staticmethod
	def _collect_100(player, state): # "xmas funds", "you inherit 100", "life insurance"
		return _collect(player, state, 100)

	@staticmethod
	def _collect_200(player, state):
		return _collect(player, state, 200)

	@staticmethod
	def _collect_50_from_every_player(player, state):
		changes_from_other_players = []
		for other_player in state.players:
			if other_player != player:
				changes_from_other_players.append(other_player.pay(player, 50, state))
		all_payments = GameStateChange.combine(changes_from_other_players)
		return all_payments

	@staticmethod
	def _pay_50(player, state):
		return player.pay(Square.BANK, 50, state)

	@staticmethod
	def _pay_100(player, state):
		return player.pay(Square.BANK, 100, state)

	@staticmethod
	def _pay_150(player, state):
		return player.pay(Square.BANK, 150, state)

	@staticmethod
	def _pay_building_fees_community_chest(player, state):
		return _pay_building_fees(player, state, COMMUNITY_CHEST_PER_HOUSE_FEE,
			COMMUNITY_CHEST_PER_HOTEL_FEE)



	# These functions make lists of lambdas for the above functions
	@staticmethod
	def _make_chance_functions():
		return [
			# Chance and community chest functions
			lambda player, state: _advance_to_go(player, state),
			lambda player, state: _go_to_jail(player, state),
			lambda player, state: _get_out_of_jail_free(player, state),

			# Chance-only functions
			lambda player, state: _collect_50(player, state),
			lambda player, state: _collect_150(player, state),
			lambda player, state: _pay_each_player_50(player, state),
			lambda player, state: _pay_poor_tax_of_15(player, state),
			lambda player, state: _pay_building_fees_chance(player, state),
			lambda player, state: _advance_to_nearest_utility(player, state),
			lambda player, state: _advance_to_nearest_railroad(player, state),
			lambda player, state: _advance_to_nearest_railroad(player, state),
			lambda player, state: _advance_to_reading_railroad(player, state),
			lambda player, state: _advance_to_boardwalk(player, state),
			lambda player, state: _advance_to_illinois_avenue(player, state),
			lambda player, state: _advance_to_st_charles_place(player, state),
			lambda player, state: _go_back_three_spaces(player, state)
		]

	@staticmethod
	def _make_community_chest_functions():
		return [
			# Chance and community chest functions
			lambda player, state: _advance_to_go(player, state),
			lambda player, state: _go_to_jail(player, state),
			lambda player, state: _get_out_of_jail_free(player, state),

			# Community-chest-only functions
			lambda player, state: _collect_10(player, state),
			lambda player, state: _collect_20(player, state),
			lambda player, state: _collect_25(player, state),
			lambda player, state: _collect_45(player, state),
			lambda player, state: _collect_100(player, state),
			lambda player, state: _collect_100(player, state),
			lambda player, state: _collect_100(player, state),
			lambda player, state: _collect_200(player, state),
			lambda player, state: _collect_50_from_every_player(player, state),
			lambda player, state: _pay_50(player, state),
			lambda player, state: _pay_100(player, state),
			lambda player, state: _pay_150(player, state),
			lambda player, state: _pay_building_fees_community_chest(player, state)
		]


	# Static decks of cards
	CHANCE_DECK = Deck(_make_chance_functions.__func__())
	COMMUNITY_CHEST_DECK = Deck(_make_community_chest_functions.__func__())



	# Instance methods
	def __init__(self, card_type):
		self._card_type = card_type

	def landed(self, player, roll, state):
		if card_type == CHANCE_CARD:
			result_of_action_on = CHANCE_DECK.draw()
		else:
			result_of_action_on = COMMUNITY_CHEST_DECK.draw()
		return result_of_action_on(player, state)



# Test client
def main():
	position = 36
	electric_company = 12
	water_works = 28
	print Card._nearest_to(position, [electric_company, water_works])

if (argv[0] == "card.py"):
	main()