class GroupOfChanges(object):

	# Takes in a list of GameStateChanges to be applied together as a unit
	def __init__(self, changes):
		self._changes = changes
