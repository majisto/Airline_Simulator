from itertools import cycle

import sge
from geopy.distance import vincenty

import global_values
import planes
from city import City
from global_values import ICON_OFFSET
from interactive_obj import I_Obj

number_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
route_arrow = "route_directional_arrow_cropped"
class Route(sge.dsp.Object):
    def __init__(self, city1, city2, distance, plane, fare, flights, num_planes, sales=0, load=0):
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

    def __init__(self, city1, city2, distance, fare_num_obj, background, objects, list_of_planes):
        super(Route_Room, self).__init__(background=background, objects=objects)
        self.list_of_planes = list_of_planes
        self.current_plane = None
        self.cycler = cycle(list_of_planes)
        self.distance = distance
        self.total_max_flights = 14
        self.current_max_flights = 1
        self.current_flights = 1
        self.num_planes = 1
        self.fare = average_fare_calculation(distance)
        self.city2 = city2
        self.city1 = city1
        self.fare_mode = False
        self.fare_num_obj = fare_num_obj
        self.cur_fare = ["$"]

    def event_room_start(self):
        self.current_plane = next(self.cycler)
        self.update_plane_box(self.current_plane)
        self.current_max_flights = flights_per_week(self.current_plane, self.distance)
        self.fare_num_obj.sprite.draw_text(global_values.text_font, "${0}".format(self.fare), 0, 0, color=global_values.text_color)
        self.update_info_boxes()

    def update_plane_box(self, plane):
        assert isinstance(plane, planes.Airplane)
        for obj in self.objects:
            if type(obj) == I_Obj:
                if obj.obj_name == "name":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "{0} {1}-{2}".format(plane.manufacturer, plane.model, plane.variant)
                                         , 0, 0, color=global_values.text_color)
                if obj.obj_name == "seats":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Seats: {0}".format(plane.seats), 0, 0, color=global_values.text_color)
                if obj.obj_name == "fuel":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Fuel: {0}".format(plane.fuel_efficiency), 0, 0, color=global_values.text_color)
                if obj.obj_name == "maintenance":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Maintenance: {0}".format(plane.maintenance), 0, 0, color=global_values.text_color)
                if obj.obj_name == "range":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Range: {0} mi".format(plane.distance), 0, 0, color=global_values.text_color)
                if obj.obj_name == "plane_count":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Count: {0}".format(global_values.player.hangar[plane.short_name])
                                         , 0, 0, color=global_values.text_color)
                if obj.obj_name == "plane_box":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "{0}".format(self.num_planes), 0, 0, color=global_values.text_color)
                if obj.obj_name == "flight_info":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Flights ({0})".format(self.current_max_flights)
                                         , 0, 0, color=global_values.text_color)

    def update_info_boxes (self):
        for obj in self.objects:
            if type(obj) == I_Obj:
                if obj.obj_name == "plane_box":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "{0}".format(self.num_planes), 0, 0,
                                         color=global_values.text_color)
                if obj.obj_name == "flight_info":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Flights ({0})".format(self.current_max_flights)
                                         , 0, 0, color=global_values.text_color)
                if obj.obj_name == "flight_box":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "{0}".format(self.current_flights)
                                     , 0, 0, color=global_values.text_color)
                if obj.obj_name == "fare_info":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, "Fare (Average: ${0})".format(self.fare),
                                         0, 0, color=global_values.text_color)

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            if obj.obj_name == "plane_plus":
                new_flight = self.current_max_flights + flights_per_week(self.current_plane, self.distance)
                if new_flight <= self.total_max_flights and self.num_planes < global_values.player.hangar[self.current_plane.short_name]:
                    self.current_max_flights = new_flight
                    self.num_planes += 1
                    self.update_info_boxes()
            if obj.obj_name == "plane_minus":
                if self.num_planes <= 1:
                    return
                new_flight = self.current_max_flights - flights_per_week(self.current_plane, self.distance)
                self.current_max_flights = new_flight
                self.current_flights = self.current_max_flights
                self.num_planes -= 1
                self.update_info_boxes()
            if obj.obj_name == "flight_plus":
                if self.current_flights < self.current_max_flights:
                    self.current_flights += 1
                    self.update_info_boxes()
            if obj.obj_name == "flight_minus":
                if self.current_flights <= 1:
                    return
                self.current_flights -= 1
                self.update_info_boxes()
            if obj.obj_name == "launch":
                if len(self.cur_fare) > 1:
                    self.fare = int(''.join(map(str, self.cur_fare[1:])))
                if global_values.debug:
                    print ("The fare is: {0}".format(self.fare))
                    print ("Current flights: {0}".format(self.current_flights))
                route = Route(self.city1, self.city2, self.distance, self.current_plane, self.fare, self.current_flights,
                              self.num_planes)
                global_values.player.route_list.append(route)
                global_values.player.money2 -= self.fare
                global_values.player.hangar[self.current_plane.short_name] -= self.num_planes
                global_values.room_dict["region"].start(transition="pixelate", transition_time=500)
            if obj.obj_name == "fare_num":
                self.fare_mode = True
                self.update_fare_number()

    def update_fare_number(self):
        self.fare_num_obj.sprite.draw_clear()
        self.fare_num_obj.sprite.draw_rectangle(0, 0, self.fare_num_obj.sprite.width - 5,
                                                self.fare_num_obj.sprite.height - 5,
                                                outline=sge.gfx.Color("gray"), outline_thickness=5)
        self.fare_num_obj.sprite.draw_text(global_values.text_font, ''.join(self.cur_fare), 0, 0,
                                           color=sge.gfx.Color('black'))

    def event_key_press(self, key, char):
        if key == "b":
            global_values.room_dict["region"].start(transition="pixelate", transition_time=500)
        elif key == "right":
            self.current_plane = next(self.cycler)
            self.num_planes = 1
            self.current_max_flights = flights_per_week(self.current_plane, self.distance)
            self.update_plane_box(self.current_plane)
        elif self.fare_mode:
            if key == "enter":
                self.fare_num_obj.sprite.draw_clear()
                self.fare_num_obj.sprite.draw_text(global_values.text_font, ''.join(self.cur_fare), 0, 0,
                                                   color=sge.gfx.Color('black'))
                return
            if len(self.cur_fare) >= 5 and key != "backspace":
                return
            if key == "backspace":
                if len(self.cur_fare) > 1:
                    del self.cur_fare[-1]
                    self.update_fare_number()
            else:
                self.cur_fare.append(key)
                self.fare_num_obj.sprite.draw_text(global_values.text_font, ''.join(self.cur_fare), 0, 0,
                                                   color=sge.gfx.Color('black'))

def create_room(city1, city2):
    distance = calculate_distance(city1, city2)
    plane_list = valid_planes(distance)
    if len(plane_list) == 0:
        raise ValueError
    calculate_total_passengers(city1, city2)
    first_city_layer, second_city_layer, route_icon_layer, top_bar_layer, name_layer, cash_layer = load_topBar(city1, city2)
    dist_icon_layer, dist_number_layer, cost_icon_layer, cost_number_layer, sprite_bar_layer = \
        cost_distance_layers(city1, city2, distance, top_bar_layer.sprite.height)
    plane_name_object, seat_object, fuel_object, maint_object, pw_obj, r_obj, cnt_obj = airplane_section()
    total_height = pw_obj.bbox_bottom
    num_p_lay, minus_obj, p_box_obj, plus_obj, flight_info, flight_minus, flight_box, flight_plus, fare_info, fare_num = flights_fare(total_height)
    new_height = total_height + flight_box.bbox_bottom
    button_obj = launch_button(new_height)

    layers = [top_bar_layer, first_city_layer, second_city_layer, route_icon_layer, name_layer, cash_layer,
              dist_icon_layer, dist_number_layer, cost_icon_layer, cost_number_layer, sprite_bar_layer, num_p_lay]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    objects = [plane_name_object, seat_object, fuel_object, maint_object, pw_obj, r_obj, cnt_obj, fare_num,
               flight_info, flight_minus, flight_box, flight_plus, minus_obj, p_box_obj, plus_obj, button_obj, fare_info]
    return Route_Room(city1, city2, distance, fare_num, background=background, objects=objects, list_of_planes=plane_list)

def launch_button(height):
    l_button = sge.gfx.Sprite(width=sge.game.width, height=100)
    l_button.draw_rectangle(0,0, l_button.width, l_button.height, outline=sge.gfx.Color("blue"), outline_thickness=5)
    l_button.draw_text(sge.gfx.Font('droid sans mono', size=40), "Launch!", 350, 0, color=sge.gfx.Color("black"))
    l_button_obj = I_Obj(0, height, sprite=l_button, obj_name="launch")
    return l_button_obj

def flights_fare(old_height):
    #Planes
    plane_box = sge.gfx.Sprite(width=200, height=30)
    num_planes = sge.gfx.Sprite(width=200, height=30)
    minus_icon = sge.gfx.Sprite("minus_icon", global_values.graphics_directory)
    plus_icon = sge.gfx.Sprite("plus_icon", global_values.graphics_directory)
    plane_num_box = sge.gfx.Sprite(width=30, height=30)

    #Flights
    flight_info = sge.gfx.Sprite(width=300, height=30)
    flight_minus_icon = sge.gfx.Sprite("minus_icon", global_values.graphics_directory)
    flight_plus_icon = sge.gfx.Sprite("plus_icon", global_values.graphics_directory)
    flight_box = sge.gfx.Sprite(width=50, height=30)

    #Fare
    fare_info = sge.gfx.Sprite(width=400, height=30)
    fare_num = sge.gfx.Sprite(width=100, height=40)

    num_planes.draw_text(global_values.text_font, "Num Planes", 0, 0, color=global_values.text_color)
    num_planes_layer = sge.gfx.BackgroundLayer(num_planes, 0, old_height)

    plane_box_obj = I_Obj(0, old_height, sprite=plane_box, obj_name="plane_box")
    minus_icon_obj = I_Obj(0, old_height + num_planes_layer.sprite.height, sprite=minus_icon, obj_name="plane_minus")
    num_box_obj = I_Obj(minus_icon_obj.bbox_width + ICON_OFFSET, minus_icon_obj.y, sprite=plane_num_box, obj_name="plane_box")
    plus_icon_obj = I_Obj(num_box_obj.x + num_box_obj.bbox_width, minus_icon_obj.y, sprite=plus_icon, obj_name="plane_plus")

    flight_info_obj = I_Obj(plane_box_obj.bbox_width + ICON_OFFSET, num_planes_layer.y, sprite=flight_info, obj_name="flight_info")
    flight_minus = I_Obj(plane_box_obj.bbox_width + ICON_OFFSET, old_height + num_planes_layer.sprite.height,
                         sprite=flight_minus_icon, obj_name="flight_minus")
    flight_box_obj = I_Obj(flight_minus.x + flight_minus.bbox_width + ICON_OFFSET, minus_icon_obj.y, sprite=flight_box, obj_name="flight_box")
    flight_plus = I_Obj(flight_box_obj.x + flight_box_obj.bbox_width, minus_icon_obj.y, sprite=flight_plus_icon, obj_name="flight_plus")

    fare_info_obj = I_Obj(flight_info_obj.bbox_width + plane_box_obj.bbox_width + ICON_OFFSET
                          , num_planes_layer.y, sprite=fare_info, obj_name="fare_info")
    fare_num_obj = I_Obj(fare_info_obj.x, num_planes_layer.y + fare_info_obj.bbox_height, sprite=fare_num, obj_name="fare_num")

    return num_planes_layer, minus_icon_obj, num_box_obj, plus_icon_obj, flight_info_obj, flight_minus\
        , flight_box_obj, flight_plus, fare_info_obj, fare_num_obj

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
                         outline=sge.gfx.Color((0, 0, 100, 30)), outline_thickness=3)

    first_city_layer = sge.gfx.BackgroundLayer(first_city, 5, 0)
    second_city_layer = sge.gfx.BackgroundLayer(second_city, sge.game.width - second_city.width, 0)
    route_icon_layer = sge.gfx.BackgroundLayer(route_icon, sge.game.width / 2.2, 0)
    top_bar_layer = sge.gfx.BackgroundLayer(top_bar, 0, 0)
    name_layer = sge.gfx.BackgroundLayer(airline_name, 0, sge.game.height - airline_name.height, 1)
    cash_layer = sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width,
                                         sge.game.height - airline_name.height, 1)

    return first_city_layer, second_city_layer, route_icon_layer, top_bar_layer, name_layer, cash_layer

def airplane_section():
    plane_window = sge.gfx.Sprite(width=sge.game.width, height=70)
    plane_name = sge.gfx.Sprite(width=280, height=30)
    seats = sge.gfx.Sprite(width=200, height=30)
    fuel_econ = sge.gfx.Sprite(width=200, height=30)
    maintenance = sge.gfx.Sprite(width=300, height=30)
    plane_range = sge.gfx.Sprite(width=300, height=30)
    plane_count = sge.gfx.Sprite(width=300, height=30)

    plane_window.draw_rectangle(0, 0, plane_window.width, plane_window.height, outline=sge.gfx.Color((0, 0, 100, 30)),
                                outline_thickness=5)

    plane_window_obj = I_Obj(0, 150, sprite= plane_window, obj_name="plane_window")
    plane_name_object = I_Obj(0, 150, sprite=plane_name, obj_name="name")
    seats_object = I_Obj(plane_name_object.x + plane_name_object.sprite.width + ICON_OFFSET, plane_name_object.y, sprite=seats, obj_name="seats")
    fuel_object = I_Obj(seats_object.x + seats_object.sprite.width , plane_name_object.y, sprite=fuel_econ, obj_name="fuel")
    maintenance_object = I_Obj(fuel_object.x + fuel_object.sprite.width , plane_name_object.y, sprite=maintenance, obj_name="maintenance")
    range_object = I_Obj(0, plane_name_object.y + plane_name_object.sprite.height, sprite=plane_range, obj_name="range")
    count_object = I_Obj(range_object.x + range_object.sprite.width + ICON_OFFSET, range_object.y, sprite=plane_count, obj_name="plane_count")

    return plane_name_object, seats_object, fuel_object, maintenance_object, plane_window_obj, range_object, count_object

def calculate_distance (city1, city2, miles=True):
    return int(vincenty(city1.lat_long, city2.lat_long).miles if miles else vincenty(city1.lat_long, city2.lat_long).kilometers)

def valid_planes(dist):
    valid = []
    for keys in global_values.player.hangar:
        if global_values.player.hangar[keys] > 0:
            # print global_values.plane_shortname_dict[keys].distance
            if int(global_values.plane_shortname_dict[keys].distance) > dist:
                valid.append(global_values.plane_shortname_dict[keys])
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
    sprite_bar.draw_line(x1=0, y1=sprite_bar.height, x2=sge.game.width, y2=sprite_bar.height,
                         color=sge.gfx.Color((0, 0, 100, 30)), thickness=3)
    dist_number.draw_text(main_font, "{0} mi".format(distance), 0,0,color=global_values.text_color)
    cost_number.draw_text(main_font, '${:0,}K'.format(cost), 0, 0, color=global_values.text_color)

    #Background layers
    sprite_bar_layer = sge.gfx.BackgroundLayer(sprite_bar, 0, prev_height)
    dist_icon_layer = sge.gfx.BackgroundLayer(dist_icon, 0, prev_height)
    dist_number_layer = sge.gfx.BackgroundLayer(dist_number, dist_icon_layer.x + dist_icon.width + ICON_OFFSET, prev_height)
    cost_icon_layer = sge.gfx.BackgroundLayer(cost_icon, sge.game.width - cost_icon.width - cost_number.width, prev_height)
    cost_number_layer = sge.gfx.BackgroundLayer(cost_number, cost_icon_layer.x + cost_icon.width + ICON_OFFSET, prev_height)
    return dist_number_layer, dist_icon_layer, cost_icon_layer, cost_number_layer, sprite_bar_layer

def flights_per_week(plane, distance):
    assert distance < plane.distance
    true_dist = distance / float (plane.distance)
    return 14 if true_dist < 0.25 else 7 if true_dist < 0.5 else 3 if true_dist < 0.90 else 1

def average_fare_calculation(distance):
    base_cost = 100
    new_cost = base_cost * (distance / 300.0)
    return int(new_cost)

def passenger_load_fare(fare, route):
    assert isinstance(route, Route)
    average_fare = average_fare_calculation(route.distance)
    total_passengers = calculate_total_passengers(route.city1, route.city2)
    updated_passengers = total_passengers / float(fare / float(average_fare))
    return updated_passengers

def calculate_total_passengers(city1, city2):
    base = 200
    assert isinstance(city1, City)
    assert isinstance(city2, City)
    city1_factor =  1.5 * (city1.tourism / 100.0) + 1.3 * (city1.population / 100.0) + 1.2 * (city1.economy / 100.0)
    city2_factor =  1.5 * (city2.tourism / 100.0) + 1.3 * (city2.population / 100.0) + 1.2 * (city2.economy / 100.0)
    print ("Total passengers for route: {0}".format(base * city1_factor * city2_factor))
    return base * city1_factor * city2_factor

def calculate_route_price(source_city, destination_city):
    #Based on population and economy of destination city
    base_cost = 3000
    population_modifier = 1000
    if global_values.debug:
        print ("Route cost: {0}".format(base_cost + (source_city.population * population_modifier + destination_city.population * population_modifier)))
    return int(base_cost + (source_city.population * population_modifier + destination_city.population * population_modifier))