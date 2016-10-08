'''
Author:   Michael Friedman
Created:	10/7/16

Description:
	Contains tests to verify the correctness of the GameState and GameStateChange
	and their operations. Uses python's built-in unittest framework.
'''

import unittest
from gamestatechange import GameStateChange
from gamestate import GameState
from player import Player
from constants import *

class TestGameState(unittest.TestCase):

	def test_creation(self):
		pass # TODO: Implement TestGameState.test_creation()


class TestGameStateChange(unittest.TestCase):

	def test_creation(self):
		pass # TODO: Implement TestGameStateChange.test_creation()

	# Create a GameStateChange that demolishes a house on a sample property, and
	# verify that it makes the appropriate changes
	def test_demolish_house(self):
		state = GameState(1)
		# Set up property to have 1 house
		boardwalk = state.squares[INDEX[BOARDWALK]]
		boardwalk.num_houses = 1

		# Construct GameStateChange
		test_gsc = GameStateChange.demolish(boardwalk)
		
		# Verify change in houses
		change_in_houses = { boardwalk: -1 }
		for prop in test_gsc.change_in_houses.keys():
			assertIn(prop, change_in_houses.keys())
			assertEquals(test_gsc.change_in_houses[prop], change_in_houses[prop])

		# Verify change in cash
		cash_transferred = boardwalk.house_price / 2
		change_in_cash = { state.get_owner(boardwalk): +cash_transferred, state.bank: -cash_transferred }
		for player in test_gsc.change_in_houses.keys():
			assertIn(player, change_in_cash.keys())
			assertEquals(test_gsc.change_in_cash[player], change_in_cash[player])

		# Verify change in houses remaining
		assertEquals(test_gsc.change_in_houses_remaining, +1)

if __name__ == '__main__':
		unittest.main()