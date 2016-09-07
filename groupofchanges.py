'''
Author:   Lenny Khazan & Michael Friedman
Created:  

Description:
	This class contains a list of GameStateChanges that should be applied as a unit.
	This is designed with the convention that the GameStateChanges will be applied
	in the order given during initialization.
'''

class GroupOfChanges(object):

	# Takes in a list of GameStateChanges to be applied together as a unit
	def __init__(self, changes=[]):
		self._changes = changes

	# Returns an iterator so this object becomes iterable
	def __iter__(self):
		return iter(self._changes)

	# Concatenates a list of GroupOfChanges objects, returns a new GroupOfChanges
	@staticmethod
	def combine(self, groups_of_changes):
		combined_group_of_changes = []
		for group_of_changes in groups_of_changes:
			combined_group_of_changes += group_of_changes
		return GroupOfChanges(combined_group_of_changes)

	def houses_built(self):
		houses = 0
		for change in self._changes:
			houses -= change.change_in_houses_remaining

		return houses

	def hotels_built(self):
		hotels = 0
		for change in self._changes:
			hotels -= change.change_in_hotels_remaining
		return hotels