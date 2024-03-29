'''
Author:   Michael Friedman
Created:  9/7/16

Description:
This object represents a Monopoly roll. It uses two dice and supports operations
for getting the value and determining whether the roll was doubles.
'''

from random import randint


class Roll(object):

  sides = 6

  @staticmethod
  def max_value():
    return 2 * Roll.sides

  def __init__(self):
    die1 = randint(1, Roll.sides)
    die2 = randint(1, Roll.sides)
    self._value = die1 + die2
    self._is_doubles = (die1 == die2)

  @property
  def value(self):
    return self._value

  @property
  def is_doubles(self):
    return self._is_doubles
