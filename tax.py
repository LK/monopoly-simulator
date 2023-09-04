from square import Square


class Tax(Square):

  def __init__(self, name, tax):
    super(Tax, self).__init__(name)
    self._tax = tax

  @property
  def tax(self):
    return self._tax

  def landed(self, player, roll, state):
    return player.pay(state.bank, self._tax, state)

  def copy(self):
    return Tax(self.name, self._tax)
