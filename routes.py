import sge
import global_values
from geopy.distance import vincenty

class Route(sge.dsp.Object):
    def __init__(self, city1, city2, distance, plane, fare, flights, num_planes, sales, load):
        super(Route, self).__init__(0, 0, visible=False)
        self.num_planes = num_planes
        self.sales = sales
        self.load = load
        self.flights = flights
        self.fare = fare
        self.plane = plane
        self.distance = distance
        self.city2 = city2
        self.city1 = city1

class Route_Room(sge.dsp.Room):

    def __init__(self, city1, city2, distance, background, objects):
        super(Route_Room, self).__init__(background=background, objects=objects)
        self.distance = distance
        self.city2 = city2
        self.city1 = city1

    def event_room_start(self):
        print self.city1.city_name

    def event_key_press(self, key, char):
        if key == "b":
            global_values.room_dict["region"].start(transition="pixelate", transition_time=500)

def create_room(city1, city2):
    distance = calculate_distance(city1, city2)
    layers = []
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Route_Room(city1, city2, distance, background=background, objects=[])

def calculate_distance (city1, city2, miles=True):
    return vincenty(city1.lat_long, city2.lat_long).miles if miles else  vincenty(city1.lat_long, city2.lat_long).kilometers