import os
import random
from math import atan2, degrees, pi

import sge

import airline_manufacturer_home
import city
import global_values
import routes
from interactive_obj import I_Obj

map_sprite_name = 'usa_canada_islands_jpeg'
route_prompt_global = None
ticket_global = None
class Region_Room(sge.dsp.Room):

    def event_room_start(self):
        self.music = sge.snd.Music(os.path.join(global_values.music_directory, "na_home_music.ogg"))
        self.music.play(loops=0)
        self.new_route_on = False
        self.route_list = []
        hub_city = self.get_hub_city()
        hub_city.sprite.draw_clear()
        hub_city.sprite.draw_ellipse(0, 0, 10, 10, fill=sge.gfx.Color((255, 71, 26)))
        for obj in self.objects:
            if type(obj) == city.City and obj.obj_name == "city":
                num_gates = obj.airport.get_gates(global_values.player.airline_name)
                obj.sprite.draw_text(sge.gfx.Font("droid sans mono", size=14), str(num_gates), 0, 12,
                                   color=global_values.text_color)

    def event_key_press(self, key, char):
        if char == "b" and self.new_route_on:
            self.clear_route()
        if char == "h":
            print (global_values.player.hangar)

    def event_room_resume(self):
        if not self.music.playing:
            self.music.play(loops=0)
        self.update_cash_display()
        for obj in self.objects[:]:
            if isinstance(obj, Plane_Sprite):
                self.remove(obj)
        for route in global_values.player.route_list:
            self.create_route_on_map(route)

    def create_route_on_map(self, route):
        if route.distance > 200:
            angle = calculate_angle(route)
            Plane_Sprite.create(route.city1.x, route.city1.y, route.city2, route.city1, rotation=angle + 45,
                                direction=angle)
        for obj in self.objects:
            if type(obj) == I_Obj and obj.obj_name == "map":
                obj.sprite.draw_line(x1=route.city1.x + 5, y1=route.city1.y + 5, x2=route.city2.x + 5,
                                     y2=route.city2.y + 5,
                                     color=global_values.text_color, thickness=1)

    def update_cash_display(self): #TODO: Make Cash and Airline Name I_OBJs for easier handling.
        self.background.layers[1].sprite.draw_clear()
        self.background.layers[1].sprite.draw_text(global_values.text_font,
                                                   '${:0,}K'.format(global_values.player.money2)
                                                   , 0, 10, color=sge.gfx.Color("red"))
        for obj in self.objects:
            if type(obj) == I_Obj:
                if obj.obj_name == "date":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, global_values.game_date.get_date(), 0, 10, color=global_values.text_color)

    def check_route_exists(self, dest_city):
        for rt in global_values.player.route_list:
            if dest_city.shortname in [rt.city1.shortname, rt.city2.shortname]:
                return True
        return False

    def clear_route(self):
        self.new_route_on = False
        route_prompt_global.sprite.draw_clear()
        ticket_global.sprite.draw_rectangle(0, 0, ticket_global.sprite.width, ticket_global.sprite.height,
                                            outline=sge.gfx.Color("white"), outline_thickness=3)

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            obj_name = obj.get_name()
            if obj_name == "city":
                if not self.new_route_on:
                    City_Room = city.create_city_room(obj)
                    City_Room.start()
                else:
                    if not self.route_check(obj):
                        self.clear_route()
                        return
                    self.clear_route()
                    try:
                        Route_Room = routes.create_room(self.get_hub_city(), obj)
                    except ValueError:
                        self.clear_route()
                        return
                    Route_Room.start()
            elif obj_name == "factory":
                Next_Room = airline_manufacturer_home.create_room()
                global_values.room_list.append(Next_Room)
                Next_Room.start()
            elif obj_name == "ticket":
                obj.sprite.draw_rectangle(0, 0, obj.sprite.width, obj.sprite.height, outline=sge.gfx.Color("blue"),
                                          outline_thickness=3)
                route_prompt_global.sprite.draw_text(global_values.small_text_font,
                        "Route starts from {0}.  Please select a destination.".format(self.get_hub_city().name_no_country), 0, 0, color=sge.gfx.Color("black"))
                self.new_route_on = True
            elif obj_name == "end":
                calculate_profit()
                global_values.game_date.advance_date()

                self.update_cash_display()

    def route_check(self, dest_city):
        if self.check_route_exists(dest_city):
            return False
        elif self.get_hub_city().airport.available_flights(global_values.player.airline_name) < 1:
            return False
        elif dest_city.airport.available_flights(global_values.player.airline_name) < 1:
            return False
        else:
            return True

    def get_hub_city(self):
        assert "region_name" in vars(self)
        return global_values.city_shortname_dict[global_values.player.hubs[self.region_name]]

class Plane_Sprite(sge.dsp.Object):

    def __init__(self, x, y, dest_city, origin_city, rotation, direction):
        plane_sprite = sge.gfx.Sprite("plane_sprite_jpeg", global_values.graphics_directory)
        super(Plane_Sprite, self).__init__(x, y, sprite=plane_sprite, image_rotation=rotation, checks_collisions=True,
                                           xvelocity=2.5, yvelocity=2.5)
        self.origin_city = origin_city
        self.dest_city = dest_city
        self.move_direction = direction
        self.moving_to = dest_city

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, city.City):
            if self.dest_city is other and self.moving_to is other:
                self.move_direction -= 180
                self.image_rotation -= 180
                self.moving_to = self.origin_city
            if self.origin_city is other and self.moving_to is other:
                self.move_direction -= 180
                self.image_rotation -= 180
                self.moving_to = self.dest_city

class Negotiation:
    gate_base_cost = 1000

    # Num_Turns: numer of turns for negotiation to work.
    def __init__(self, num_turns, num_gates, acity, airline_name):
        self.airline_name = airline_name
        self.acity = acity
        self.num_turns = num_turns
        self.num_gates = num_gates
        self.cost = Negotiation.gate_base_cost * num_gates

    @staticmethod
    def buy_gates(acity, airline_name, hub):
        max_gates = acity.airport.available_gates(airline_name, hub)
        return max_gates

    def resolve_negotiation(self):
        self.num_turns -= 1
        if self.num_turns == 0:
            self.acity.airport.add_gates(self.airline_name, self.num_gates)
            return True
        return False

    def calculate_length(self, acity):
        return acity.relations + (1 if random.random() < 0.05 else 0)

def create_room():
    global route_prompt_global
    global ticket_global
    # Sprites
    airline_name = sge.gfx.Sprite(width=250, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)
    date_sprite = sge.gfx.Sprite(width=170, height=50)
    cash_font = sge.gfx.Font("droid sans mono", size=30)
    factory = sge.gfx.Sprite("factory_cropped", global_values.graphics_directory)
    ticket = sge.gfx.Sprite("ticket_cropped", global_values.graphics_directory)
    end_turn = sge.gfx.Sprite("end_button", global_values.graphics_directory)
    negotiation = sge.gfx.Sprite("negotiation", global_values.graphics_directory)
    background_map = sge.gfx.Sprite(map_sprite_name, global_values.graphics_directory)
    prompt = sge.gfx.Sprite(width=750, height=50)

    airline_name.draw_text(cash_font, global_values.player.airline_name, 0, 10, color=sge.gfx.Color("red"))
    airline_cash.draw_text(global_values.text_font, '${:0,}K'.format(global_values.player.money2), 0, 10, color=sge.gfx.Color("red"),
                           halign='left')
    date_sprite.draw_text(global_values.text_font, global_values.game_date.get_date(), 0, 10, color=global_values.text_color)

    name_layer = sge.gfx.BackgroundLayer(airline_name, 0, background_map.height, 1)
    cash_layer = sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width,
                                      background_map.height, 1)
    factory_object = I_Obj(name_layer.x + name_layer.sprite.width, name_layer.y, sprite=factory, obj_name="factory",
                           active=False, tangible=False)
    ticket_object = I_Obj(factory_object.x + factory_object.bbox_width + global_values.ICON_OFFSET,
                          factory_object.y, sprite=ticket, obj_name="ticket", active=False, tangible=False)
    end_turn_object = I_Obj(ticket_object.x + ticket_object.bbox_width + global_values.ICON_OFFSET, factory_object.y,
                            sprite=end_turn, obj_name="end", active=False, tangible=False)
    negotiation_obj = I_Obj(end_turn_object.bbox_right + global_values.ICON_OFFSET, factory_object.y, sprite=negotiation, obj_name="negotiation",
                            active=False, tangible=False)
    prompt_object = I_Obj(200, sge.game.height - airline_name.height - prompt.height,
                          sprite=prompt, obj_name="prompt", z=2)
    route_prompt_global = prompt_object
    ticket_global = ticket_object #TODO: This is janky.  Figure out a better way than a global.
    map_object = I_Obj(0, 0, sprite=background_map, obj_name="map", z=-10, active=False, tangible=False)
    date_object = I_Obj(cash_layer.x - date_sprite.width, factory_object.y, sprite=date_sprite, obj_name="date", active=False, tangible=False)

    object_list = get_cities()
    object_list.extend((factory_object, ticket_object, prompt_object, map_object, end_turn_object, negotiation_obj, date_object))
    layers = [name_layer, cash_layer]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Region_Room(background=background, objects=object_list)

def calculate_profit():
    for route in global_values.player.route_list:
        total_seats = int(route.plane.seats) * route.num_planes
        total_passengers = int(routes.calculate_total_passengers(route.city1, route.city2))
        averaging_fare = int(routes.passenger_load_fare(route.fare, route))
        if total_passengers >= total_seats:
            if averaging_fare > route.fare:
                sales = route.fare * total_seats
            else:
                sales = averaging_fare * total_seats
        else:
            if averaging_fare > route.fare:
                sales = route.fare * (total_seats - total_passengers)
            else:
                sales = averaging_fare * (total_seats - total_passengers)
        global_values.player.money2 += sales
        if global_values.debug:
            print ("Total sales is {0} on route to {1}".format(sales, route.city2.name_no_country))

def calculate_angle(route):
    dx = route.city2.x - route.city1.x
    dy = route.city2.y - route.city1.y
    rads = atan2(dy, dx)
    rads %= 2 * pi
    degs = degrees(rads)
    return degs

def get_cities():
    o_list = []
    for local_city in global_values.city_list:
        o_list.append(local_city)
    return o_list