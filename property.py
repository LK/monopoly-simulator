from square import Square

class Property(Square):
	def __init__(self, price, rents, property_group, properties_in_group=3,
							 mortgaged=False):
		self._price = price
		self._rents = rents
		self._property_group = property_group
		self._properties_in_group = properties_in_group
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
	def properties_in_group(self):
		return self._properties_in_group

	@property
	def mortgaged(self):
		return self._mortgaged
	
	@mortgaged.setter
	def mortgaged(self, mortgaged):
		self._mortgaged = mortgaged