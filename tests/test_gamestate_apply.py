'''
Author:   Michael Friedman
Created:	10/7/16

Description:
	Contains tests to verify that all GameStateChanges are applied correctly
	by GameState.apply(). Uses python's built-in unittest framework.
'''

import unittest
import difflib
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from gamestate import GameState
from player import Player
from constants import *

class TestGameStateApply(unittest.TestCase):

	'''
	Helper function for computing the difference between two GameStates' string
	encodings.

	Takes two strings s1, s2 as arguments and returns a list of 2-tuples of differing
	lines between s1 and s2. The first item in each tuple is the line from the first
	string, and the second item is the (differing) line from the second string.
	Assumes s1 and s2 have the same number of lines, and raises an exception if
	they don't.
	
	Ex:
		> s = diff('Name: Park Place\nNum Houses: 1\nMortgaged: False\n',
						 'Name: Boardwalk\nNum Houses: 2\nMortgaged: False\n')
		> print s
		[('Name: Park Place', 'Name: Boardwalk'),
		 ('Num Houses: 1', Num Houses: 2')]
	'''
	def diff(self, s1, s2):
		l1 = s1.splitlines()
		l2 = s2.splitlines()
		if len(l1) != len(l2):
			raise Exception('Number of lines in each string is different')

		# Form 2-tuples of lines from s1 and s2
		diff = []
		for i in range(0, len(l1)):
			if l1[i] != l2[i]:
				diff.append((l1[i], l2[i]))
		return diff


	'''
	Helper function for computing the difference between two GameStates.

	Takes two strings str_before and str_after, the string encodings of the
	GameStates before and after applying a changes, the list expected_diff of
	of 2-tuples containing differing lines (in the same format returned by diff()),
	and checks that the difference between str_before and str_after (computed with
	diff()) matches expected_diff. If not, raises an assertion error and prints
	the string msg, along with the actual unified difference between the two strings
	and the expected_diff.
	'''
	def assertDiffGameStates(self, str_before, str_after, expected_diff, msg=''):
		test_diff = self.diff(str_before, str_after)
		unified_diff = ''.join(difflib.unified_diff(str_before.splitlines(1),
			str_after.splitlines(1)))
		self.assertEqual(test_diff, expected_diff,
			msg=msg + '\n\nExpected Diff:\n%s \n\nActual Unified Diff:\n%s'
			% (str(expected_diff), unified_diff))


	'''
	Apply a GameStateChange that transfers money from the bank to a player.
	Test that the resulting GameState is correct.
	'''
	def test_transfer_money_bank_to_player(self):
		import random

		state = GameState(1)
		player = state.players[0]

		# Transfer random amounts of money, and test that GameState is correct
		for trial in range(0, 100):
			player_cash_before = player.cash
			bank_cash_before = state.bank.cash
			amount = random.randint(1, player_cash_before)

			str_before = str(state)
			state.apply(GroupOfChanges([
				GameStateChange.transfer_money(state.bank, player, amount)]))
			str_after = str(state)
			expected_diff = [
				# Player cash
				('Cash: %d' % player_cash_before,
				 'Cash: %d' % (player_cash_before + amount)),

				# Bank cash
				('Cash: %d' % bank_cash_before,
				 'Cash: %d' % (bank_cash_before - amount))
			]
			self.assertDiffGameStates(str_before, str_after, expected_diff,
				msg='$%d was not transferred to player correctly. Here is diff:' % amount)


	'''
	Apply a GameStateChange that transfers money from a player to the bank.
	Test that the resulting GameState is correct.
	'''
	def test_transfer_money_player_to_bank(self):
		import random

		state = GameState(1)
		player = state.players[0]

		# Transfer random amounts of money, and test that GameState is correct
		for trial in range(0, 100):
			# Restock player if he runs out during trials
			if player.cash == 0:
				player.cash = 1500

			# Test transfer
			player_cash_before = player.cash
			bank_cash_before = state.bank.cash
			amount = random.randint(1, player_cash_before)

			str_before = str(state)
			state.apply(GroupOfChanges([
				GameStateChange.transfer_money(player, state.bank, amount)]))
			str_after = str(state)
			expected_diff = [
				# Player cash
				('Cash: %d' % player_cash_before,
				 'Cash: %d' % (player_cash_before - amount)),

				# Bank cash
				('Cash: %d' % bank_cash_before,
				 'Cash: %d' % (bank_cash_before + amount))
			]
			self.assertDiffGameStates(str_before, str_after, expected_diff,
				msg='$%d was not transferred to the bank correctly. Here is diff:' % amount)


	'''
	Apply a GameStateChange that transfers money from a player to another
	player. Test that the resulting GameState is correct.
	'''
	def test_transfer_money_player_to_player(self):
		import random

		state = GameState(2)

		# Transfer money, and test that GameState is correct
		for trial in range(0, 100):
			# Restock players if they run out of cash during trials
			for i in range(0, 2):
				if state.players[i].cash == 0:
					state.players[i].cash = 1500

			# Test transfer
			cash_before = [0] * 2
			for i in range(0, 2):
				cash_before[i] = state.players[i].cash

			pfrom = random.randint(0, 1)
			pto = 1 - pfrom
			amount = random.randint(1, cash_before[pfrom])

			str_before = str(state)
			state.apply(GroupOfChanges([
				GameStateChange.transfer_money(state.players[pfrom], state.players[pto],
					amount)
			]))
			str_after = str(state)
			expected_diff = [
				# pfrom cash
				('Cash: %d' % cash_before[pfrom],
				 'Cash: %d' % (cash_before[pfrom] - amount)),

				# pto cash
				('Cash: %d' % cash_before[pto],
				 'Cash: %d' % (cash_before[pto] + amount))
			]

			# Player stats must be listed in numerical order, so swap the order
			# if pfrom is not the 0'th player
			if pfrom == 1:
				expected_diff.reverse()

			self.assertDiffGameStates(str_before, str_after, expected_diff,
				msg='$%d was not transferred between players correctly. Here is diff:' % amount)


	'''
	Apply a GameStateChange that transfers a property (a purple) from one player to
	another player. Test that the resulting GameState is correct.
	'''
	def test_transfer_property(self):
		state = GameState(2)
		player1 = state.players[0]
		player2 = state.players[1]

		# Set up player1 to have the purples, player2 to have the railroads
		purples = [MEDITERRANEAN_AVENUE, BALTIC_AVENUE]
		changes = []
		for prop_name in purples:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player1, state.bank))

		state.apply(GroupOfChanges(changes))

		railroads = [READING_RAILROAD, PENNSYLVANIA_RAILROAD, B_AND_O_RAILROAD,
			SHORT_LINE_RAILROAD]
		changes = []
		for prop_name in railroads:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player2, state.bank))

		state.apply(GroupOfChanges(changes))		

		# Transfer property
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.transfer_property(player1, player2,
				state.squares[INDEX[BALTIC_AVENUE]])
		]))	
		str_after = str(state)
		expected_diff = [
			# Player 1 stats
			('Mediterranean Avenue, Baltic Avenue, ', 'Mediterranean Avenue, '),
			('0: 2', '0: 1'),

			# Player 2 properties
			('Reading Railroad, Pennsylvania Railroad, B. & O. Railroad, Short Line Railroad, ', 'Reading Railroad, Pennsylvania Railroad, B. & O. Railroad, Short Line Railroad, Baltic Avenue, '),
			('0: 0', '0: 1')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Baltic Avenue was not transferred properly')


	'''
	Apply a GameStateChange that buys a property (a green) from the bank for a
	player as the player's first property. Test that the resulting GameState
	is correct.	
	'''
	def test_buy_property_from_nothing(self):
		state = GameState(1)
		player = state.players[0]

		# Test buying Pacific Avenue
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(state.squares[INDEX[PACIFIC_AVENUE]],
				player, state.bank)
		]))
		str_after = str(state)
		expected_diff = [
			# Player 1 stats
			('Cash: 1500', 'Cash: 1200'),
			('', 'Pacific Avenue, '),
			('6: 0', '6: 1'),

			# Bank stats
			('Cash: 0', 'Cash: 300'),
			('Mediterranean Avenue, Baltic Avenue, Reading Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, St. Charles Place, Electric Company, States Avenue, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, Pacific Avenue, North Carolina Avenue, Pennsylvania Avenue, Short Line Railroad, Park Place, Boardwalk, ',
			 'Mediterranean Avenue, Baltic Avenue, Reading Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, St. Charles Place, Electric Company, States Avenue, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, North Carolina Avenue, Pennsylvania Avenue, Short Line Railroad, Park Place, Boardwalk, '),
			('6: 3', '6: 2')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Pacific Avenue was not purchased properly')


	'''
	Apply a GameStateChange that buys a property (a green) from the bank for a
	player after he has already purchased some properties. Test that the
	resulting GameState is correct.	
	'''
	def test_buy_property_from_something(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player with some properties (two of the three greens)
		changes = []
		for prop_name in [PACIFIC_AVENUE, PENNSYLVANIA_AVENUE]:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank))

		state.apply(GroupOfChanges(changes))

		# Test buying North Carolina Avenue
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(state.squares[INDEX[NORTH_CAROLINA_AVENUE]],
				player, state.bank)
		]))
		str_after = str(state)
		expected_diff = [
			# Player 1 stats
			('Cash: 880', 'Cash: 580'), 
			('Pacific Avenue, Pennsylvania Avenue, ', 'Pacific Avenue, Pennsylvania Avenue, North Carolina Avenue, '),
			('6: 2', '6: 3'),

			# Bank stats
			('Cash: 620', 'Cash: 920'),
			('Mediterranean Avenue, Baltic Avenue, Reading Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, St. Charles Place, Electric Company, States Avenue, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, North Carolina Avenue, Short Line Railroad, Park Place, Boardwalk, ',
			 'Mediterranean Avenue, Baltic Avenue, Reading Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, St. Charles Place, Electric Company, States Avenue, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, Short Line Railroad, Park Place, Boardwalk, '),
			('6: 1', '6: 0')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='North Carolina Avenue was not purchased properly')


	'''
	Applies a GameStateChange that buys a property (a green) mortgaged for a
	player. Tests that the resulting GameState is correct.
	'''
	def test_buy_property_mortgaged(self):
		state = GameState(1)
		player = state.players[0]

		# Test buying Pennsylvania Avenue mortgaged
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(state.squares[INDEX[PENNSYLVANIA_AVENUE]],
				player, state.bank, mortgaged=True)
		]))
		str_after = str(state)
		expected_diff = [
			# Player stats
			('Cash: 1500', 'Cash: 1340'),
			('', 'Pennsylvania Avenue, '),
			('6: 0', '6: 1'),

			# Bank stats
			('Cash: 0', 'Cash: 160'),
			('Mediterranean Avenue, Baltic Avenue, Reading Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, St. Charles Place, Electric Company, States Avenue, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, Pacific Avenue, North Carolina Avenue, Pennsylvania Avenue, Short Line Railroad, Park Place, Boardwalk, ',
				'Mediterranean Avenue, Baltic Avenue, Reading Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, St. Charles Place, Electric Company, States Avenue, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, Pacific Avenue, North Carolina Avenue, Short Line Railroad, Park Place, Boardwalk, '),
			('6: 3', '6: 2'),

			# Pennsylvania Avenue stats
			('Mortgaged: False', 'Mortgaged: True')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Pennsylvania Avenue was not mortgaged properly')


	'''
	Apply a GameStateChange that moves a player to some new position from the
	initial position (Go). Test that the resulting GameState is correct.	
	'''
	def test_change_position_from_start(self):
		state = GameState(1)
		player = state.players[0]

		# Test player changing position from initial position (Go) to first 
		# Chance square
		chance1 = INDEX[CHANCE_1]

		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, chance1, state.bank, state.squares)
		]))
		str_after = str(state)
		expected_diff = [
			('Position: 0', 'Position: %d' % chance1)
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player was not moved to first Chance square properly')


	'''
	Apply a GameStateChange that moves a player to some new position from a
	square in the middle of the board. Test that the resulting GameState is
	correct.	
	'''
	def test_change_position_from_middle(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player's initial position at Community Chest 2
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[COMMUNITY_CHEST_2], state.bank,
				state.squares)
		]))

		# Test player changing position to Water Works
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[WATER_WORKS], state.bank,
				state.squares)
		]))
		str_after = str(state)
		expected_diff = [
			('Position: %d' % INDEX[COMMUNITY_CHEST_2],
			 'Position: %d' % INDEX[WATER_WORKS])
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player was not moved from Community Chest 2 to Water Works properly')


	'''
	Apply a GameStateChange that moves a player from a square before Go to a
	square after Go. Test that the resulting GameState is correct.
	'''
	def test_change_position_passing_go(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player's initial position at Short Line Railroad
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[SHORT_LINE_RAILROAD], state.bank,
				state.squares)
		]))

		# Test player changing position to Reading Railroad
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[READING_RAILROAD], state.bank,
				state.squares)
		]))
		str_after = str(state)
		expected_diff = [
			# Player stats
			('Position: %d' % INDEX[SHORT_LINE_RAILROAD],
			 'Position: %d' % INDEX[READING_RAILROAD]),
			('Cash: 1500', 'Cash: 1700'),

			# Bank stats
			('Cash: 0', 'Cash: -200')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player did not pass Go properly')


	'''
	Apply a GameStateChange that moves a player from a square before Go to Go.
	Test that the resulting GameState is correct.
	'''
	def test_change_position_landing_on_go(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player's initial position at Short Line Railroad
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[SHORT_LINE_RAILROAD], state.bank,
				state.squares)
		]))

		# Test player changing position to Go
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[GO], state.bank, state.squares)
		]))
		str_after = str(state)
		expected_diff = [
			# Player stats
			('Position: %d' % INDEX[SHORT_LINE_RAILROAD],
			 'Position: %d' % INDEX[GO]),
			('Cash: 1500', 'Cash: 1700'),

			# Bank stats
			('Cash: 0', 'Cash: -200')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player did not pass Go properly')


	'''
	Apply a GameStateChange that mortgages an unmortgaged property (a railroad).
	Test that the resulting GameState is correct.
	'''
	def test_mortgage(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player to own a railroad
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(state.squares[INDEX[PENNSYLVANIA_RAILROAD]],
				player, state.bank)
		]))

		# Test mortgage
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.mortgage(state.squares[INDEX[PENNSYLVANIA_RAILROAD]], state)
		]))
		str_after = str(state)
		expected_diff = [
			# Player cash
			('Cash: 1300', 'Cash: 1400'),

			# Bank cash
			('Cash: 200', 'Cash: 100'),

			# Pennsylvania Railroad stats
			('Mortgaged: False', 'Mortgaged: True')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Pennsylvania Railroad was not mortgaged properly')


	'''
	Apply a GameStateChange that unmortgages an mortgaged property (a utility).
	Test that the resulting GameState is correct.
	'''
	def test_unmortgage(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player to own a mortgaged utility
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(state.squares[INDEX[ELECTRIC_COMPANY]],
				player, state.bank, mortgaged=True)
		]))

		# Test unmortgage
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.unmortgage(state.squares[INDEX[ELECTRIC_COMPANY]], state)
		]))
		str_after = str(state)
		expected_diff = [
			# Player cash
			('Cash: 1425', 'Cash: 1342'),

			# Bank cash
			('Cash: 75', 'Cash: 158'),

			# Electric Company stats
			('Mortgaged: True', 'Mortgaged: False')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Electric Company was not unmortgaged properly')	


	'''
	Apply a GameStateChange that builds a house on the oranges. Test that the
	resulting GameState is correct.
	'''
	def test_build_house(self):
		state = GameState(1)

		# Set up a player to own oranges with no houses
		player = state.players[0]
		oranges = [ST_JAMES_PLACE, TENNESSEE_AVENUE, NEW_YORK_AVENUE]
		
		changes = []
		for prop_name in oranges:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank))

		state.apply(GroupOfChanges(changes))

		# Test house build
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.build(state.squares[INDEX[NEW_YORK_AVENUE]], state)
		]))
		str_after = str(state)
		expected_diff = [
			('Cash: 940', 'Cash: 840'),          # player cash
			('Cash: 560', 'Cash: 660'),          # bank cash
			('Num houses: 0', 'Num houses: 1'),  # new york avenue
			('Houses remaining: 32', 'Houses remaining: 31')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='House build was not applied properly')


	'''
	Apply a GameStateChange that builds a hotel on the reds. Test that the resulting
	GameState is correct.
	'''
	def test_build_hotel(self):
		state = GameState(1)

		# Set up a player to own reds with 4 houses each
		player = state.players[0]
		reds = [KENTUCKY_AVENUE, INDIANA_AVENUE, ILLINOIS_AVENUE]

		state.apply(GroupOfChanges([
			GameStateChange.transfer_money(state.bank, player, 1130) # needs $1130 more to buy everything
		]))

		changes = []
		for prop_name in reds:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank))

		state.apply(GroupOfChanges(changes))

		for count in range(0, 4):
			for prop_name in reds:
				state.apply(GroupOfChanges([
					GameStateChange.build(state.squares[INDEX[prop_name]], state)
				]))

		# Test hotel build
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.build(state.squares[INDEX[INDIANA_AVENUE]], state)
		]))
		str_after = str(state)
		expected_diff = [
			('Cash: 150', 'Cash: 0'),
			('Cash: 1350', 'Cash: 1500'),
			('Num houses: 4', 'Num houses: 5'),
			('Houses remaining: 20', 'Houses remaining: 24'),
			('Hotels remaining: 12', 'Hotels remaining: 11')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Hotel build was not applied properly')


	'''
	Apply a GameStateChange that demolishes a house on the dark blues. Test that
	the resulting GameState is correct.
	'''
	def test_demolish_house(self):
		state = GameState(1)

		# Set up a player to own a property with 1 house
		player = state.players[0]
		park_place = state.squares[INDEX[PARK_PLACE]]
		boardwalk = state.squares[INDEX[BOARDWALK]]
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(park_place, player, state.bank)]))
		state.apply(GroupOfChanges([
			GameStateChange.buy_property(boardwalk, player, state.bank)]))
		state.apply(GroupOfChanges([
			GameStateChange.build(boardwalk, state)]))

		# Test applying the changes by comparing differences in their string
		# encodings. Ensure that no additional changes were made to the state.
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.demolish(boardwalk, state)]))
		str_after = str(state)
		expected_diff = [
			('Cash: 550', 'Cash: 650'),  # player cash
			('Cash: 950', 'Cash: 850'),  # bank cash
			('Num houses: 1', 'Num houses: 0'),
			('Houses remaining: 31', 'Houses remaining: 32')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='House demolition was not applied correctly')


	'''
	Apply a GameStateChange that demolishes a hotel on the pinks. Test that the
	resulting GameState is correct
	'''
	def test_demolish_hotel(self):
		state = GameState(1)

		# Set up a player to own a property group with hotels on all properties
		player = state.players[0]
		state.apply(GroupOfChanges([
			GameStateChange.transfer_money(state.bank, player, 440)])) # Needs 440 more to buy everything
		pinks = [ST_CHARLES_PLACE, STATES_AVENUE, VIRGINIA_AVENUE]
		changes = []
		for prop_name in pinks:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank))

		state.apply(GroupOfChanges(changes))

		for i in range(0, 5):
			for prop_name in pinks:
				state.apply(GroupOfChanges([
					GameStateChange.build(state.squares[INDEX[prop_name]], state)
				]))

		# Test demolition
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.demolish(state.squares[INDEX[ST_CHARLES_PLACE]], state)
		]))
		str_after = str(state)
		expected_diff = [
			('Cash: 0', 'Cash: 50'),            # player cash
			('Cash: 1500', 'Cash: 1450'),       # bank cash
			('Num houses: 5', 'Num houses: 4'), # st charles place
			('Houses remaining: 32', 'Houses remaining: 28'),
			('Hotels remaining: 9', 'Hotels remaining: 10')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Hotel demolition was not applied correctly')


	'''
	Apply a GameStateChange that draws a card from Chance and Community Chest
	decks. Test that the resulting GameStates are correct.
	'''
	def test_draw_card(self):
		state = GameState(1)
		player = state.players[0]

		# Test every card in both decks
		dict_card_types = { CHANCE_CARD: 'Chance', COMMUNITY_CHEST_CARD: 'Community Chest' }
		for card_type, card_str in dict_card_types.items():
			deck = state.decks[card_type]

			# Draw every card in the deck, check that cards are handled correctly
			# and that nothing else in the state is changed
			card = None
			for i in range(0, deck.size()):
				card = deck.peek()
				jail_free_count_before = player.jail_free_count
				str_before = str(state)
				expected_diff = None  # initialized in the following if-block

				state.apply(GroupOfChanges([
					GameStateChange.draw_card(deck, player)]))
				if card == LMBDA_GET_OUT_OF_JAIL_FREE:
					# Check that the card is not replaced on the deck, and that the
					# player's Jail Free card count is incremented.
					self.assertEqual(player.jail_free_count, jail_free_count_before + 1)
					for j in range(0, deck.size()):
						self.assertNotEqual(deck.draw(), LMBDA_GET_OUT_OF_JAIL_FREE)

					# Initialize. Used after this if-block to ensure that nothing else
					# in the state was changed.
					expected_diff = [
						('Jail free count: %d' % jail_free_count_before,
						 'Jail free count: %d' % player.jail_free_count)
					]
				else:
					# Check that the card is replaced on the bottom if it is not the
					# Jail Free card.
					for j in range(0, deck.size() - 1):
						deck.draw()
					self.assertEqual(deck.draw(), card) # compare with last card

					# Initialize
					expected_diff = []

				# Check that the rest of the state is unchanged by comparing the
				# string encodings of the GameStates
				str_after = str(state)
				self.assertDiffGameStates(str_before, str_after, expected_diff,
					msg='The GameState was not modified correctly')


	'''
	Apply a GameStateChange that decrements number of jail cards in a player's
	hand and replaces the card to the appropriate deck. Test that the resulting
	GameState is correct.
	'''
	def test_decrement_jail_card_count(self):
		state = GameState(1)
		player = state.players[0]

		# Test both decks
		dict_card_types = { CHANCE_CARD: 'Chance', COMMUNITY_CHEST_CARD: 'Community Chest' }
		for card_type, card_str in dict_card_types.items():
			deck = state.decks[card_type]

			# Set up a player to have a 'Get out of jail free' card
			while deck.peek() != LMBDA_GET_OUT_OF_JAIL_FREE:
				state.apply(GroupOfChanges([
					GameStateChange.draw_card(deck, player)]))
			state.apply(GroupOfChanges([
				GameStateChange.draw_card(deck, player)])) # draw Jail Free card

			# Test difference in jail card count by looking at the difference in
			# GameStates' string encodings. Ensure that only the jail card count was
			# changed.
			str_before = str(state)
			state.apply(GroupOfChanges([
				GameStateChange.decrement_jail_card_count(player, deck)]))
			str_after = str(state)
			expected_diff = [
				('Jail free count: 1', 'Jail free count: 0')
			]
			self.assertDiffGameStates(str_before, str_after, expected_diff,
				msg='Jail free count was not decremented correctly')

			# Test that the Jail Free card was placed back on the bottom of the deck,
			# and that no additional copies of the Jail Free card are in the deck
			count = 0
			for i in range(0, deck.size() - 1):
				card = deck.draw()  # draw all cards except last one
				if card == LMBDA_GET_OUT_OF_JAIL_FREE:
					count += 1
			self.assertEqual(count, 0,
				msg='Another Get out of jail free card is in the middle of the %s deck' % card_str)
			self.assertEqual(deck.peek(), LMBDA_GET_OUT_OF_JAIL_FREE,
				msg='Get out of jail free card was not replaced into %s deck' % card_str)


	'''
	Apply a GameStateChange that sends a player to jail. Test that the resulting
	GameState is correct.
	'''
	def test_send_to_jail(self):
		state = GameState(1)
		player = state.players[0]

		# Send the player to jail, and compare GameState's string encodings to
		# ensure that only the player's position was changed
		position_before = player.position
		position_jail = INDEX[JAIL]
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.send_to_jail(player)]))
		str_after = str(state)
		expected_diff = [
		 	('Position: %d' % position_before, 'Position: %d' % position_jail),
		 	('Jail moves: 0', 'Jail moves: 3')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player was not sent to jail properly')


	'''
	Apply a GameStateChange that decrements a player's jail moves. Test that the
	resulting GameState is correct.
	'''
	def test_decrement_jail_moves(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player in jail
		state.apply(GroupOfChanges([
			GameStateChange.send_to_jail(player)]))
		
		# Decrement jail moves, and test that the player's jail moves were changed
		# correctly and that no other changes were made to the state.
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.decrement_jail_moves(player)]))
		str_after = str(state)
		expected_diff = [
			('Jail moves: 3', 'Jail moves: 2')
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player jail moves were not decremented properly')


	'''
	Apply a GameStateChange that releases a player from jail. Test that the
	resulting GameState is correct.
	'''
	def test_leave_jail(self):
		state = GameState(1)
		player = state.players[0]

		# Test that leaving jail works no matter how many jail moves are left
		for num_turns in range(0, 3):
			# Set up player in jail
			state.apply(GroupOfChanges([
				GameStateChange.send_to_jail(player)]))

			# Decrement player's jail moves num_turns (0, 1, or 2) times
			for i in range(0, num_turns):
				state.apply(GroupOfChanges([
					GameStateChange.decrement_jail_moves(player)]))

			# Test leaving jail, and ensure that player's jail moves are changed
			# correctly and that no other changes were made to the state.
			str_before = str(state)
			state.apply(GroupOfChanges([
				GameStateChange.leave_jail(player)]))
			str_after = str(state)
			expected_diff = [
				('Jail moves: %d' % (3-num_turns), 'Jail moves: 0')
			]
			self.assertDiffGameStates(str_before, str_after, expected_diff,
				msg='Player did not leave jail properly')


	'''
	Applies changes to the GameState state that set up player 0 with the following:
	the 3-house level on the light blues, mortgaged states avenue and short line
	railroad, and the chance Jail Free card. He is left with whatever cash is
	leftover from his original 1500 after all of these purchases.
	'''
	def setup_eliminated_player(self, state):
		player = state.players[0]
		light_blues = [ORIENTAL_AVENUE, VERMONT_AVENUE, CONNECTICUT_AVENUE]

		# Give player properties
		changes = []
		for prop_name in light_blues:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank))

		state.apply(GroupOfChanges(changes))


		# Build to 3 house level on light blues
		for count in range(0, 3):
			for prop_name in light_blues:
				state.apply(GroupOfChanges([
					GameStateChange.build(state.squares[INDEX[prop_name]], state)
				]))

		# Give player some other properties mortgaged
		changes = []
		other_props = [STATES_AVENUE, SHORT_LINE_RAILROAD]
		for prop_name in other_props:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank, mortgaged=True))

		state.apply(GroupOfChanges(changes))

		# Give player a Jail Free card
		changes = []
		deck = state.decks[CHANCE_CARD]
		while deck.peek() != LMBDA_GET_OUT_OF_JAIL_FREE:
			deck.draw()
		changes.append(GameStateChange.draw_card(deck, player)) # draw Jail Free card

		state.apply(GroupOfChanges(changes))


	'''
	Applies changes to the GameState state that set up player 1 with the following:
	the 3-house level on the yellows, and readling, pennsylvania, and b&o
	railroads. He is left with whatever cash is left over after these purchases,
	starting with $3000. Assumes that the player has only his initial $1500 in
	the state provided.
	'''
	def setup_eliminator_player(self, state):
		player = state.players[1]
		yellows = [ATLANTIC_AVENUE, VENTNOR_AVENUE, MARVIN_GARDENS]
		railroads = [READING_RAILROAD, PENNSYLVANIA_RAILROAD, B_AND_O_RAILROAD]
		changes = []

		# Add to player's initial $1500 to bring him to $3000 cash
		changes.append(GameStateChange.transfer_money(state.bank, player, 1500))

		# Give player properties
		for prop_name in yellows + railroads:
			changes.append(GameStateChange.buy_property(state.squares[INDEX[prop_name]],
				player, state.bank))

		state.apply(GroupOfChanges(changes))

		# Build to 3 house level on yellows
		for count in range(0, 3):
			for prop_name in yellows:
				state.apply(GroupOfChanges([
					GameStateChange.build(state.squares[INDEX[prop_name]], state)
				]))


	'''
	Apply a GameStateChange that eliminates a player from the game, losing to
	the bank. Test that the resulting GameState is correct.
	'''
	def test_eliminate_to_bank(self):
		state = GameState(1)
		player = state.players[0]

		# Set up player to have some clout
		self.setup_eliminated_player(state)

		# Move player to a square where he would likely lose to the bank (e.g.
		# Luxury Tax)
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player, INDEX[LUXURY_TAX], state.bank,
			state.squares)
		]))

		# Eliminate the player to the bank, and test that the player's belongings
		# are properly transferred to the bank and that no other changes are
		# made to the state.
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.eliminate(player, state.bank, state)]))
		str_after = str(state)
		expected_diff = [
			# Player stats
			('Position: %d' % INDEX[LUXURY_TAX], 'Position: -1'),
			('Cash: 560', 'Cash: 0'),
			('Oriental Avenue, Vermont Avenue, Connecticut Avenue, States Avenue, Short Line Railroad, ', ''),
			('1: 3', '1: 0'),
			('2: 1', '2: 0'),
			('100: 1', '100: 0'),
			('Jail free count: 1', 'Jail free count: 0'),
			('Is in game: True', 'Is in game: False'),

			# Bank stats
			('Cash: 940', 'Cash: 1725'),
			('Mediterranean Avenue, Baltic Avenue, Reading Railroad, St. Charles Place, Electric Company, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, Pacific Avenue, North Carolina Avenue, Pennsylvania Avenue, Park Place, Boardwalk, ',
			 'Mediterranean Avenue, Baltic Avenue, Reading Railroad, St. Charles Place, Electric Company, Virginia Avenue, Pennsylvania Railroad, St. James Place, Tennessee Avenue, New York Avenue, Kentucky Avenue, Indiana Avenue, Illinois Avenue, B. & O. Railroad, Atlantic Avenue, Ventnor Avenue, Water Works, Marvin Gardens, Pacific Avenue, North Carolina Avenue, Pennsylvania Avenue, Park Place, Boardwalk, Oriental Avenue, Vermont Avenue, Connecticut Avenue, States Avenue, Short Line Railroad, '),
			('1: 0', '1: 3'),
			('2: 2', '2: 3'),
			('100: 3', '100: 4'),

			# Property stats
			('Num houses: 3', 'Num houses: 0'),      # Oriental Avenue
			('Num houses: 3', 'Num houses: 0'),      # Vermont Avenue
			('Num houses: 3', 'Num houses: 0'),      # Connecticut Avenue
			('Mortgaged: True', 'Mortgaged: False'), # States Avenue
			('Mortgaged: True', 'Mortgaged: False'), # Short Line Railroad

			# Housing stats
			('Houses remaining: 23', 'Houses remaining: 32')  # 9 houses from light blues
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player was not eliminated properly. The following changes were made to the GameState:')


	'''
	Apply a GameStateChange that eliminates a player from the game, losing to
	another player. Test that the resulting GameState is correct.
	'''
	def test_eliminate_to_player(self):
		state = GameState(2)
		player_eliminated = state.players[0]
		player_eliminator = state.players[1]

		# Set up players to have some clout
		self.setup_eliminated_player(state)
		self.setup_eliminator_player(state)

		# Move player_eliminated to a square where he would likely lose to the
		# other player (e.g. Marvin Gardens)
		state.apply(GroupOfChanges([
			GameStateChange.change_position(player_eliminated, INDEX[MARVIN_GARDENS],
				state.bank, state.squares)
		]))

		# Eliminate player_eliminated to player_eliminator, and test that
		# player_eliminated's belongings are properly transferred to the
		# player_eliminator and that no other changes are made to the state.
		str_before = str(state)
		state.apply(GroupOfChanges([
			GameStateChange.eliminate(player_eliminated, player_eliminator, state)]))
		str_after = str(state)
		expected_diff = [
			# Eliminated player stats
			('Position: %d' % INDEX[MARVIN_GARDENS], 'Position: -1'),
			('Cash: 560', 'Cash: 0'),
			('Oriental Avenue, Vermont Avenue, Connecticut Avenue, States Avenue, Short Line Railroad, ', ''),
			('1: 3', '1: 0'),
			('2: 1', '2: 0'),
			('100: 1', '100: 0'),
			('Jail free count: 1', 'Jail free count: 0'),
			('Is in game: True', 'Is in game: False'),

			# Eliminator player stats
			('Cash: 250', 'Cash: 1035'),
			('Atlantic Avenue, Ventnor Avenue, Marvin Gardens, Reading Railroad, Pennsylvania Railroad, B. & O. Railroad, ',
			 'Atlantic Avenue, Ventnor Avenue, Marvin Gardens, Reading Railroad, Pennsylvania Railroad, B. & O. Railroad, Oriental Avenue, Vermont Avenue, Connecticut Avenue, States Avenue, Short Line Railroad, '),
			('1: 0', '1: 3'),
			('2: 0', '2: 1'),
			('100: 3', '100: 4'),
			('Jail free count: 0', 'Jail free count: 1'),

			# Property stats
			('Num houses: 3', 'Num houses: 0'),      # Oriental Avenue
			('Num houses: 3', 'Num houses: 0'),      # Vermont Avenue
			('Num houses: 3', 'Num houses: 0'),      # Connecticut Avenue

			# Housing stats
			('Houses remaining: 14', 'Houses remaining: 23')  # 9 houses from light blues
		]
		self.assertDiffGameStates(str_before, str_after, expected_diff,
			msg='Player was not eliminated properly. The following changes were made to the GameState:')

#-------------------------------------------------------------------------------

'''
Main script. Run with
	python test_gamestate_apply.py
to debug with pdb.
'''
import pdb 

if __name__ == '__main__':
	pdb.set_trace()
	unittest.main()