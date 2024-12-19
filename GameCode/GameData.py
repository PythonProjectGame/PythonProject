class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5
        self.ui.create_hearts(self._health)
        self._dead = False

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, val):
        self._coins = val
        if self._coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, val):
        self._health = val
        self.ui.create_hearts(val)
        if self._health <= 0:
            self._dead = True

    @property
    def dead(self):
        return self._dead

    @dead.setter
    def dead(self, val):
        self._dead = val
