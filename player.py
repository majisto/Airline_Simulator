import sge

class Player(sge.dsp.Object):
    def __init__(self, money, airline_name):
        super(Player, self).__init__(self, 0, 0, tangible=False, visible=False)
        self.money = money
        self.airline_name = airline_name