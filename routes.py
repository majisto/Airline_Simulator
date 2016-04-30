import sge

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
