class NotificationChanges(object):
	def __init__(self, non_building_changes, building_requests):
		self._non_building_changes = non_building_changes
		self._building_requests = building_requests

	@property
	def non_building_changes(self):
		return self._non_building_changes
	
	@property
	def building_requests(self):
		return self._building_requests
	