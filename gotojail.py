from square import Square
from gamestatechange import GameStateChange
from groupofchanges import GroupOfChanges


class GoToJail(Square):
    def __init__(self, name):
        super(GoToJail, self).__init__(name)

    def landed(self, player, roll, state):
        return GroupOfChanges(changes=[GameStateChange.send_to_jail(player)])
