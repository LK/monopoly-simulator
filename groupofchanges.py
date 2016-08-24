class GroupOfChanges(object):

	# Takes in a list of GameStateChanges to be applied together as a unit
	def __init__(self, changes=[]):
		self._changes = changes

	# Concatenates a list of GroupOfChanges objects, returns a new GroupOfChanges
	@staticmethod
	def combine(self, groups_of_changes):
		combined_group_of_changes = []
		for group_of_changes in groups_of_changes:
			combined_group_of_changes += group_of_changes
		return GroupOfChanges(combined_group_of_changes)
