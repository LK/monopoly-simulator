'''
Author:   Lenny Khazan
Created:  

Description:
Notifications are broadcasted to Players by the Engine to make them aware of
the current GameState. Players are able to submit changes they wish to make
upon seeing the current GameState. The NotificationChanges object is a container
for these changes/requests submitted by a Player in response to a notification.
'''

from buildingrequests import BuildingRequests

class NotificationChanges(object):
	def __init__(self, non_building_changes=[], building_requests=BuildingRequests()):
		self._non_building_changes = non_building_changes
		self._building_requests = building_requests

	@property
	def non_building_changes(self):
		return self._non_building_changes
	
	@property
	def building_requests(self):
		return self._building_requests
	