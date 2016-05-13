import sge

class Player(sge.dsp.Object):
    def __init__(self, money, airline_name, money2):
        super(Player, self).__init__(self, 0, 0, tangible=False, visible=False)
        self.money2 = money2
        self.money = money
        self.airline_name = airline_name
        self.hangar = {} #Key: Plane shortname Value: Number of that plane