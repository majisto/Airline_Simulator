import sge
from global_values import ICON_OFFSET
import global_values
from geopy.distance import vincenty

route_arrow = "route_directional_arrow_cropped"
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
        print self.city1.full_name

    def event_key_press(self, key, char):
        if key == "b":
            global_values.room_dict["region"].start(transition="pixelate", transition_time=500)

def create_room(city1, city2):
    distance = calculate_distance(city1, city2)
    valid_planes(distance)
    first_city_layer, second_city_layer, route_icon_layer, top_bar_layer, name_layer, cash_layer = load_topBar(city1, city2)
    dist_icon_layer, dist_number_layer, cost_icon_layer, cost_number_layer = cost_distance_layers(city1, city2, distance, top_bar_layer.sprite.height)

    layers = [top_bar_layer, first_city_layer, second_city_layer, route_icon_layer, name_layer, cash_layer,
              dist_icon_layer, dist_number_layer, cost_icon_layer, cost_number_layer]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Route_Room(city1, city2, distance, background=background, objects=[])

def load_topBar(city1, city2):
    larger_font = sge.gfx.Font("droid sans mono", size=30)
    airline_name = sge.gfx.Sprite(width=250, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)
    top_bar = sge.gfx.Sprite(width=sge.game.width, height=70)
    first_city = sge.gfx.Sprite(width=300, height=top_bar.height)
    second_city = sge.gfx.Sprite(width=300, height=top_bar.height)
    route_icon = sge.gfx.Sprite(route_arrow, global_values.graphics_directory)

    airline_name.draw_text(global_values.cash_font, global_values.player.airline_name, 0, 10,
                           color=sge.gfx.Color("red"))
    airline_cash.draw_text(global_values.cash_font, '${:0,}K'.format(global_values.player.money2), 0, 10,
                           color=sge.gfx.Color("red"),
                           halign='left')
    first_city.draw_text(larger_font, city1.full_name, 0, 0, color=global_values.text_color)
    second_city.draw_text(larger_font, city2.full_name, 0, 0, color=global_values.text_color)
    top_bar.draw_polygon([(sge.game.width, 0), (sge.game.width, top_bar.height), (0, top_bar.height), (0, 0)],
                         outline=sge.gfx.Color((0, 0, 100, 30)), outline_thickness=5)

    first_city_layer = sge.gfx.BackgroundLayer(first_city, 5, 0)
    second_city_layer = sge.gfx.BackgroundLayer(second_city, sge.game.width - second_city.width, 0)
    route_icon_layer = sge.gfx.BackgroundLayer(route_icon, sge.game.width / 2.2, 0)
    top_bar_layer = sge.gfx.BackgroundLayer(top_bar, 0, 0)
    name_layer = sge.gfx.BackgroundLayer(airline_name, 0, sge.game.height - airline_name.height, 1)
    cash_layer = sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width,
                                         sge.game.height - airline_name.height, 1)

    return first_city_layer, second_city_layer, route_icon_layer, top_bar_layer, name_layer, cash_layer

def calculate_distance (city1, city2, miles=True):
    return int(vincenty(city1.lat_long, city2.lat_long).miles if miles else vincenty(city1.lat_long, city2.lat_long).kilometers)

def valid_planes(dist):
    print dist
    valid = []
    for keys in global_values.player.hangar:
        if global_values.player.hangar[keys] > 0:
            # print global_values.plane_shortname_dict[keys].distance
            if int(global_values.plane_shortname_dict[keys].distance) > dist:
                valid.append(global_values.plane_shortname_dict[keys])
    for plane in valid:
        print plane.model
    return valid

def cost_distance_layers(city1, city2, distance, prev_height):
    cost = calculate_route_price(city1, city2)
    #Sprites
    dist_icon = sge.gfx.Sprite("route_distance", global_values.graphics_directory)
    cost_icon = sge.gfx.Sprite("economy_icon_small", global_values.graphics_directory)
    sprite_bar = sge.gfx.Sprite(width=sge.game.width, height=dist_icon.height)
    dist_number = sge.gfx.Sprite(width=250, height=dist_icon.height)
    cost_number = sge.gfx.Sprite(width=250, height=cost_icon.height)
    main_font = sge.gfx.Font('droid sans mono', size=sprite_bar.height)
    dist_number.draw_text(main_font, "{0} mi".format(distance), 0,0,color=global_values.text_color)
    cost_number.draw_text(main_font, '${:0,}K'.format(cost), 0, 0, color=global_values.text_color)

    #Background layers
    dist_icon_layer = sge.gfx.BackgroundLayer(dist_icon, 0, prev_height)
    dist_number_layer = sge.gfx.BackgroundLayer(dist_number, dist_icon_layer.x + dist_icon.width + ICON_OFFSET, prev_height)
    cost_icon_layer = sge.gfx.BackgroundLayer(cost_icon, sge.game.width - cost_icon.width - cost_number.width, prev_height)
    cost_number_layer = sge.gfx.BackgroundLayer(cost_number, cost_icon_layer.x + cost_icon.width + ICON_OFFSET, prev_height)
    return dist_number_layer, dist_icon_layer, cost_icon_layer, cost_number_layer

def calculate_route_price(source_city, destination_city):
    #Based on population and economy of destination city
    base_cost = 3000
    population_modifier = 1000
    if global_values.debug:
        print "Route cost: {0}".format(base_cost + (source_city.population * population_modifier + destination_city.population * population_modifier))
    return int(base_cost + (source_city.population * population_modifier + destination_city.population * population_modifier))