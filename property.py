from square import Square

class Property(Square):

	# Initialize a property
	# price: (int) 					Amount a Player must pay to buy the property
	#
	# rents: (int[])				Amounts a Player must pay when landing on the property,
	#												indexed by either num of houses on it (color properties)
	#												or num of that property group owned (non-color properties)
	#
	# property_group: (int)	A label from 0-9 indicating the group this property
	#												belongs to
	#
	# size_of_property_group: (int)	Num of properties in the group this property
	#																belongs to
	# mortgaged: (boolean)	Indicates mortgage status of this property
	def __init__(self, name, price, rents, property_group, size_of_property_group=3,
							 mortgaged=False):
		super(Property, self).__init__(name)
		
		self._price = price
		self._rents = rents
		self._property_group = property_group
		self._size_of_property_group = size_of_property_group
		self._mortgaged = mortgaged

	@property
	def price(self):
		return self._price

	@price.setter
	def price(self, price):
		self._price = price

	@property
	def rents(self):
		return self._rents

	@property
	def property_group(self):
		return self._property_group

	@property
	def size_of_property_group(self):
		return self._size_of_property_group

	@property
	def mortgaged(self):
		return self._mortgaged
	
	@mortgaged.setter
	def mortgaged(self, mortgaged):
		self._mortgaged = mortgaged