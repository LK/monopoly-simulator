class Player(object):
    def __init__(self):
        self.money = 1500
        self.jailTimeRemaining = 0
        self.properties = []

    def pay(self, money):
        if self.money >= money:
            self.money -= money
            return True
        else:
            # TODO: Mortgage
            return False

    def receive(self, money):
        self.money += money
