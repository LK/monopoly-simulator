from square import Square
from deck import Deck
from gamestatechange import GameStateChange
from gotojail import GoToJail
from roll import Roll
from groupofchanges import GroupOfChanges
from constants import *

class Card(Square):

	# Chance and community chest functions
	@staticmethod
	def _advance_to_square(player, square_index, roll, state):
		state.apply(GameStateChange.change_position(player, square_index, state.bank, state.squares))
		square = state.squares[square_index]
		return square.landed(player, roll, state)

	@staticmethod
	def _advance_to_go(player, state):
		return Card._advance_to_square(player, INDEX[GO], 0, state)

	@staticmethod
	def _go_to_jail(player, state):
		go_to_jail = state.squares[INDEX[GO_TO_JAIL]]
		return jail.landed(player, 0, state)

	@staticmethod
	def _pay_building_fees(player, state, per_house_fee, per_hotel_fee):
		total_houses = 0
		total_hotels = 0
		for prop in player.props:
			if isinstance(prop, ColorProperty):
				if prop.has_hotel():
					total_hotels += 1
				else:
					total_houses += prop.num_houses()
		fee = (total_houses * per_house_fee) + (total_hotels * per_hotel_fee)
		return player.pay(state.bank, fee, state)

	@staticmethod
	def _collect(player, amount, state):
		transfer_money = GameStateChange.transfer_money(state.bank, player, amount)
		return GroupOfChanges([transfer_money])

	@staticmethod
	def _pay(player_from, player_to, amount, state):
		return player_from.pay(player_to, amount, state)

	@staticmethod
	def _get_out_of_jail_free(player, state):
		return GroupOfChanges() # 'jail free' card is handled by GameStateChange.draw_card()



	# Chance-only functions
	@staticmethod
	def _collect_50(player, state):
		return Card._collect(player, 50, state)

	@staticmethod
	def _collect_150(player, state):
		return Card._collect(player, 150, state)

	@staticmethod
	def _pay_each_player_50(player, state):
		changes_paying_players = []
		for other_player in state.players:
			if other_player != player:
				changes_paying_players.append(player.pay(other_player, 50, state))
		all_payments = GroupOfChanges.combine(changes_paying_players)
		return all_payments

	@staticmethod
	def _pay_poor_tax_of_15(player, state):
		return Card._pay(player, state.bank, 15, state)

	@staticmethod
	def _pay_building_fees_chance(player, state):
		return Card._pay_building_fees(player, state, CHANCE_PER_HOUSE_FEE,
			CHANCE_PER_HOTEL_FEE)


	# Helper function for "advance to nearest __________" cards.
	# Returns the square nearest to the given position going forward
	@staticmethod
	def _nearest_to(position, square_indices):
		min_dist = NUM_SQUARES + 1
		nearest = square_indices[0]
		for square_index in square_indices:
			if square_index - position < 0:
				# Account for going around the board mod 40
				dist_to_go = -position % NUM_SQUARES
				dist = dist_to_go + square_index
			else:
				dist = square_index - position

			if dist < min_dist:
				min_dist = dist
				nearest = square_index
		return nearest

	@staticmethod
	def _advance_to_nearest_utility(player, state):
		electric_company 	= INDEX[ELECTRIC_COMPANY]
		water_works 			= INDEX[WATER_WORKS]
		nearest_utility 	= Card._nearest_to(player.position, [electric_company,
			water_works])
		roll = Roll().value
		return Card._advance_to_square(player, nearest_utility, roll, state)  # TODO: Always make rent roll x 10

	@staticmethod
	def _advance_to_nearest_railroad(player, state):
		reading_railroad 			= INDEX[READING_RAILROAD]
		pennsylvania_railroad	= INDEX[PENNSYLVANIA_RAILROAD]
		b_and_o_railroad 			= INDEX[B_AND_O_RAILROAD]
		short_line_railroad 	= INDEX[SHORT_LINE_RAILROAD]
		nearest_railroad 			= Card.nearest_to(player.position, [reading_railroad,
			pennsylvania_railroad, b_and_o_railroad, short_line_railroad])
		return Card._advance_to_square(player, nearest_railroad, 0, state)

	@staticmethod
	def _advance_to_reading_railroad(player, state):
		return Card._advance_to_square(player, INDEX[READING_RAILROAD], 0, state)

	@staticmethod
	def _advance_to_boardwalk(player, state):
		return Card._advance_to_square(player, INDEX[BOARDWALK], 0, state)

	@staticmethod
	def _advance_to_illinois_avenue(player, state):
		return Card._advance_to_square(player, INDEX[ILLINOIS_AVENUE], 0, state)

	@staticmethod
	def _advance_to_st_charles_place(player, state):
		return Card._advance_to_square(player, INDEX[ST_CHARLES_PLACE], 0, state)

	@staticmethod
	def _go_back_three_spaces(player, state):
		change_position = GameStateChange.change_position(player, player.position - 3, state.bank, state.squares)
		return GroupOfChanges([change_position])




	# Community-chest-only functions
	@staticmethod
	def _collect_10(player, state):
		return Card._collect(player, 10, state)

	@staticmethod
	def _collect_20(player, state):
		return Card._collect(player, 20, state)

	@staticmethod
	def _collect_25(player, state):
		return Card._collect(player, 25, state)

	@staticmethod
	def _collect_45(player, state):
		return Card._collect(player, 45, state)

	@staticmethod
	def _collect_100(player, state): # "xmas funds", "you inherit 100", "life insurance"
		return Card._collect(player, 100, state)

	@staticmethod
	def _collect_200(player, state):
		return Card._collect(player, 200, state)

	@staticmethod
	def _collect_50_from_every_player(player, state):
		changes_from_other_players = []
		for other_player in state.players:
			if other_player != player:
				changes_from_other_players.append(other_player.pay(player, 50, state))
		all_payments = GroupOfChanges.combine(changes_from_other_players)
		return all_payments

	@staticmethod
	def _pay_50(player, state):
		return Card._pay(player, state.bank, 50, state)

	@staticmethod
	def _pay_100(player, state):
		return Card._pay(player, state.bank, 100, state)

	@staticmethod
	def _pay_150(player, state):
		return Card._pay(player, state.bank, 150, state)

	@staticmethod
	def _pay_building_fees_community_chest(player, state):
		return Card._pay_building_fees(player, state, COMMUNITY_CHEST_PER_HOUSE_FEE,
			COMMUNITY_CHEST_PER_HOTEL_FEE)

	@staticmethod
	def make_chance_functions():
		return [
			# Chance and community chest functions
			lambda player, state: Card._advance_to_go(player, state),
			lambda player, state: Card._go_to_jail(player, state),
			LMBDA_GET_OUT_OF_JAIL_FREE,

			# Chance-only functions
			lambda player, state: Card._collect_50(player, state),
			lambda player, state: Card._collect_150(player, state),
			lambda player, state: Card._pay_each_player_50(player, state),
			lambda player, state: Card._pay_poor_tax_of_15(player, state),
			lambda player, state: Card._pay_building_fees_chance(player, state),
			lambda player, state: Card._advance_to_nearest_utility(player, state),
			lambda player, state: Card._advance_to_nearest_railroad(player, state),
			lambda player, state: Card._advance_to_nearest_railroad(player, state),
			lambda player, state: Card._advance_to_reading_railroad(player, state),
			lambda player, state: Card._advance_to_boardwalk(player, state),
			lambda player, state: Card._advance_to_illinois_avenue(player, state),
			lambda player, state: Card._advance_to_st_charles_place(player, state),
			lambda player, state: Card._go_back_three_spaces(player, state)
		]

	@staticmethod
	def make_community_chest_functions():
		return [
			# Chance and community chest functions
			lambda player, state: Card._advance_to_go(player, state),
			lambda player, state: Card._go_to_jail(player, state),
			LMBDA_GET_OUT_OF_JAIL_FREE,

			# Community-chest-only functions
			lambda player, state: Card._collect_10(player, state),
			lambda player, state: Card._collect_20(player, state),
			lambda player, state: Card._collect_25(player, state),
			lambda player, state: Card._collect_45(player, state),
			lambda player, state: Card._collect_100(player, state),
			lambda player, state: Card._collect_100(player, state),
			lambda player, state: Card._collect_100(player, state),
			lambda player, state: Card._collect_200(player, state),
			lambda player, state: Card._collect_50_from_every_player(player, state),
			lambda player, state: Card._pay_50(player, state),
			lambda player, state: Card._pay_100(player, state),
			lambda player, state: Card._pay_150(player, state),
			lambda player, state: Card._pay_building_fees_community_chest(player, state)
		]



	# Instance methods
	def __init__(self, name, card_type):
		super(Card, self).__init__(name)
		self._card_type = card_type

	def landed(self, player, roll, state):
		deck = state.decks[self._card_type]
		draw_card = GameStateChange.draw_card(deck, player)
		card_lmbda = draw_card.card_drawn[deck]
		result_of_card = card_lmbda(player, state)
		return GroupOfChanges.combine([GroupOfChanges([draw_card]), result_of_card])



# Test client
def main():
	position = 36
	electric_company = 12
	water_works = 28
	print Card._nearest_to(position, [electric_company, water_works])

if __name__ == '__main__':
	main()