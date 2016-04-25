import sge

class City(sge.dsp.Object):

    def __init__(self, name, coordinates, region, population, tourism, economy, sprite):
        super(City, self).__init__(x=coordinates[0], y=coordinates[1], sprite=sprite)
        self.economy = economy
        self.tourism = tourism
        self.population = population
        self.region = region
        self.city_name = name
    pass

class City_Room(sge.dsp.Room):

    def __init__(self, City_Class):
        super(City_Room, self).__init__()
        self.city = City_Class
    pass

def create_city_room(City_Class):
    return City_Room(City_Class)