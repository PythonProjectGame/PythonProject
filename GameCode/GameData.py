class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5
        self.ui.createHearts(self._health)

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, val):
        self._coins = val
        if self._coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.showCoins(self.coins)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, val):
        self._health = val
        self.ui.createHearts(val)
