import csv
import random

import sge

import global_values
from global_values import ICON_OFFSET
from interactive_obj import Hud_Obj

POP_ICON_FILENAME = 'population_icon'
ECON_ICON_FILENAME = 'economy_icon_cropped'

city_list = []
city_dict = {}
city_shortname_dict = {}
base_gate_number = 40
MAX_GATES = 14

class City(sge.dsp.Object):

    def __init__(self, name, coordinates, region, population, tourism, economy, lat_long, name_no_country,
                 obj_name="city", sprite=None, shortname=""):
        super(City, self).__init__(x=coordinates[0], y=coordinates[1], sprite=sprite, active=False, checks_collisions=False)
        self.name_no_country = name_no_country
        self.obj_name = obj_name
        self.economy = economy
        self.tourism = tourism
        self.population = population
        self.region = region
        self.full_name = name
        self.lat_long = lat_long
        self.shortname = shortname
        self.airport = Airport(self)
        self.relations = {global_values.player.airline_name:global_values.relation_dict["great"]}
        if global_values.debug:
            self.airport.add_gates(global_values.player.airline_name, 0)

    def get_name(self):
        return self.obj_name

    def change_relation(self, airline_name, relation):
        self.relations[airline_name] = relation

def create_cities():
    if city_list is None or len(city_list) == 0:
        with open("City_Master_List.csv", "r") as f:
            cities = csv.reader(f, dialect='excel')
            cityiter = iter(cities)
            next(cityiter)
            for l in cityiter:
                name_no_country = l[0]
                name = l[0] + "\n" + l[1]
                #Cast to int because they are read in as string.  I spent way too many hours debugging this!
                coordinates = tuple([int(i) for i in l[2].split(",")])
                region = l[3]
                population = float(l[4])
                tourism = int(l[5])
                economy = int(l[6])
                shortname = l[7]
                lat_long = tuple([float(i) for i in l[8].split(",")])
                city_dot = sge.gfx.Sprite(width=25, height=25)
                city_dot.draw_ellipse(0, 0, 10, 10, fill=sge.gfx.Color("green"))
                # city_dot.draw_text(sge.gfx.Font("droid sans mono", size=11), "999", 0, 10, color=global_values.text_color)
                city = City(name, coordinates, region, population, tourism, economy, lat_long, name_no_country,
                                      shortname=shortname, sprite=city_dot)
                city_list.append(city)
                if region in city_dict:
                    city_dict[region].append(city)
                else:
                    city_dict[region] = [city]
        global_values.city_dict = city_dict
        global_values.city_list = city_list
        for city in city_list:
            city_shortname_dict[city.shortname] = city
        global_values.city_shortname_dict = city_shortname_dict
    return city_list

if __name__ == '__main__':
    create_cities()

class City_Room(sge.dsp.Room):

    def __init__(self, City_Class, background, objects, negotiation_array=None, neg_obj=None, neg_prompt = None):
        super(City_Room, self).__init__(background=background, objects=objects)
        self.neg_obj = neg_obj
        if negotiation_array is None:
            negotiation_array = []
        self.city = City_Class
        self.negotiation_array = negotiation_array
        self.negotiation_index = 0
        self.submit = False
        self.negotiation = None
        self.neg_prompt = neg_prompt

    def event_key_press(self, key, char):
        if key == "g":
            print (self.city.airport.available_gates(global_values.player.airline_name, True))
        if key == "b":
            global_values.room_dict["region"].start()
        if key =="n":
            s = sge.gfx.Sprite("person_negotiate", global_values.graphics_directory)
            self.city.sprite.draw_sprite(s, 0, 10, 0)
        if key == "e":
            self.city.sprite.draw_erase(10, 0, 15, 15)
        if key =="right":
            if len(self.negotiation_array) == 0:
                return
            self.add_gate()
        if key == "left":
            if len(self.negotiation_array) == 0:
                return
            self.subtract_gate()

    def subtract_gate(self):
        self.negotiation_array[self.negotiation_index].visible = False
        if self.negotiation_index > 0:
            self.negotiation_index -= 1
        self.update_negotiation_object()

    def add_gate(self):
        if self.negotiation_index < len(self.negotiation_array) - 1:
            self.negotiation_index += 1
        self.negotiation_array[self.negotiation_index].visible = True
        self.update_negotiation_object()

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            obj_name = obj.get_name()
            if obj_name == "plus_icon":
                self.add_gate()
            if obj_name == "minus_icon":
                self.subtract_gate()
            if obj_name == "submit":
                if self.submit:
                    global_values.player.negotiation_list.append(self.negotiation)
                    global_values.room_dict["region"].start()
                else:
                    self.negotiation = Negotiation(Negotiation.calculate_length(self.city), self.negotiation_index, self.city, global_values.player.airline_name)
                    self.neg_prompt.sprite.draw_text(global_values.smaller_text_font, "Negotiations will take {0} month{1}.  Click submit again to confirm.".format(self.negotiation.num_turns, "s" if self.negotiation.num_turns > 1 else ""),
                                                     0, 0, color=global_values.text_color)
                    self.submit = True

    def update_negotiation_object(self):
        self.neg_obj.sprite.draw_clear()
        self.neg_obj.sprite.draw_text(global_values.text_font, "({0})".format(self.negotiation_index), 0, 0, color=global_values.text_color)

    def event_room_start(self):
        self.update_negotiation_object()
        for obj in self.objects:
            if type(obj) == Hud_Obj:
                if obj.obj_name == "pop":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.population) + "M", 0, obj.sprite.height / 4,
                                         color=sge.gfx.Color("black"))
                elif obj.obj_name == "econ":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.economy), 0, obj.sprite.height / 4,
                                         color=sge.gfx.Color("black"))
                elif obj.obj_name == "full_name":
                    obj.sprite.draw_clear()
                    city_font = sge.gfx.Font("droid sans mono", size=40)
                    obj.sprite.draw_rectangle(0, 0, obj.sprite.width, obj.sprite.height ,
                                              outline=sge.gfx.Color("gray"), outline_thickness=2)
                    obj.sprite.draw_text(city_font, self.city.full_name, global_values.game.width / 3,0,
                                         color=sge.gfx.Color("black"))
                elif obj.obj_name == "tour":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.tourism), 0, obj.sprite.height / 4,
                                         color=sge.gfx.Color("black"))


class Airport:
    """
    Used to keep track of gates for a city.  Manages total gates, gates per airline and expansion
    .. attribute:: city

        City object the gate will be added to.
    """
    def __init__(self, city):
        self.total_gates = Airport.calculate_total(city)
        self.total_used = 0
        #Key: Airline Name Value: List [0] = Used Gates for flights [1] = Total Gates owned
        self.gate_dict = {}

    @staticmethod
    def calculate_total(acity):
        assert isinstance(acity, City)
        return int(base_gate_number + acity.population * 2.5 + (acity.tourism / 4.0))

    def get_gates(self, airline_name):
        if airline_name in self.gate_dict:
            return self.gate_dict[airline_name][1]
        else:
            self.gate_dict[airline_name] = [0, 0]
            return 0

    def get_flights(self, airline_name):
        if airline_name in self.gate_dict:
            return self.gate_dict[airline_name][0]
        else:
            self.gate_dict[airline_name] = [0, 0]
            return 0

    def available_flights(self, airline_name):
        return self.gate_dict[airline_name][1] - self.gate_dict[airline_name][0]

    def available_gates(self, airline_name, hub):
        if hub:
            assert airline_name in self.gate_dict
            #Check if enough gates are left.
            if self.total_gates * 0.75 >= self.total_used:
                a = int(self.total_gates * 0.75 - self.total_used)
                return a if a < 14 else 14
            else:
                return 0
        else:
            if self.total_gates * 0.5 >= self.total_used:
                a = int(self.total_gates * 0.5 - self.total_used)
                return a if a < 14 else 14
            else:
                return 0

    def add_gates(self, airline_name, num_gates):
        num_gates = int(num_gates)
        if airline_name in self.gate_dict:
            self.gate_dict[airline_name][1] += num_gates
        else:
            self.gate_dict[airline_name] = [0, num_gates]

    def add_flights(self, airline_name, num_flights):
        assert num_flights + self.gate_dict[airline_name][0] <= self.gate_dict[airline_name][1]
        self.total_used += num_flights
        self.gate_dict[airline_name][0] += num_flights

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

    @staticmethod
    def calculate_length(acity):
        return acity.relations[global_values.player.airline_name] + (1 if random.random() < 0.05 else 0)

def create_city_room(City_Class, negotiation):

    #Sprites
    population_icon = sge.gfx.Sprite(POP_ICON_FILENAME, global_values.graphics_directory)
    economy_icon = sge.gfx.Sprite(ECON_ICON_FILENAME, global_values.graphics_directory)
    tourism_icon = sge.gfx.Sprite("tourism_cropped", global_values.graphics_directory)
    city_image = sge.gfx.Sprite("austin_texas_cropped", global_values.city_image_directory)
    country_flag = sge.gfx.Sprite("us_flag_cropped", global_values.flags_directory, transparent=False)
    population_number = sge.gfx.Sprite(width=90, height=population_icon.height)
    economy_number = sge.gfx.Sprite(width=60, height=economy_icon.height)
    tourism_number = sge.gfx.Sprite(width=60, height=tourism_icon.height)
    city_name = sge.gfx.Sprite(width=sge.game.width, height=90)
    relation = sge.gfx.Sprite("hand_shake_cropped", global_values.graphics_directory)
    num_bound_box = sge.gfx.Sprite(width=sge.game.width, height=population_icon.height)
    airline_name = sge.gfx.Sprite(width=200, height=30)
    airline_cash = sge.gfx.Sprite(width=200, height=30)

    #Bottom Bar
    airline_name.draw_text(global_values.text_font, global_values.player.airline_name, 0, 0, color=sge.gfx.Color("red"))
    airline_cash.draw_text(global_values.text_font, '${:0,}K'.format(global_values.player.money2), 0, 0,
                           color=sge.gfx.Color("red"),
                           halign='left')

    #Objects/Layers
    layers = [sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width, sge.game.height - airline_name.height)]

    airline_name_obj = Hud_Obj(0, sge.game.height - airline_name.height, airline_name, "airline_name")
    city_name_object = Hud_Obj(0, 0, city_name, "full_name", z=10)
    flag_object = Hud_Obj(0,0, country_flag, "flag", z=11)
    relation_object = Hud_Obj(global_values.game.width - 100,0, relation, "relation", z=11)

    #Pop/Tour/Econ objects
    population_obj = Hud_Obj(0, flag_object.bbox_bottom, population_icon)
    population_number_object = Hud_Obj(population_obj.bbox_width + ICON_OFFSET, flag_object.bbox_bottom,
                                       population_number, "pop", z=1)
    economy_number_object = Hud_Obj(sge.game.width - economy_number.width, flag_object.bbox_bottom, economy_number, "econ")
    econ_obj = Hud_Obj(economy_number_object.bbox_left - economy_icon.width - ICON_OFFSET, flag_object.bbox_bottom,
                       economy_icon)
    tourism_obj = Hud_Obj((sge.game.width / 2.0) - population_obj.bbox_right, flag_object.bbox_bottom,
                          tourism_icon)
    tourism_number_object = Hud_Obj(tourism_obj.bbox_right + ICON_OFFSET, flag_object.bbox_bottom, tourism_number, "tour")
    num_bound_box_obj = Hud_Obj(0, 100, sprite=num_bound_box, obj_name="numbers_box")
    city_image_obj = Hud_Obj(0, num_bound_box_obj.bbox_bottom, city_image)

    #Gate Objects
    tot_name_obj, tot_gate_obj, fst_name, fst_gate = airport_graphics(city_image_obj.bbox_bottom, City_Class)

    flight_sprite = sge.gfx.Sprite("plane_sprite", global_values.graphics_directory, width=30, height=30)

    object_list = [population_number_object, economy_number_object, city_name_object, flag_object,
                   relation_object, tourism_number_object, tot_name_obj, tot_gate_obj, fst_gate, fst_name,
                   city_image_obj, population_obj, econ_obj, tourism_obj, airline_name_obj]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))

    negotiation_planes, neg_obj, neg_prompt = negotiation_objects(flight_sprite, negotiation, object_list, tot_gate_obj, airline_name_obj)
    return City_Room(City_Class, background=background, objects=object_list, negotiation_array=negotiation_planes, neg_obj=neg_obj,
                     neg_prompt=neg_prompt)


def negotiation_objects(flight_sprite, negotiation, object_list, tot_gate_obj, air_name_obj):
    if negotiation:
        neg_text = sge.gfx.Sprite(width=300, height=30)
        neg_text.draw_text(global_values.text_font, "Number of gates", 0, 0, color=global_values.text_color)
        neg_text_obj = Hud_Obj(0, tot_gate_obj.bbox_bottom, neg_text)
        minus_icon = sge.gfx.Sprite("minus_icon", global_values.graphics_directory)
        minus_icon_obj = Hud_Obj(neg_text_obj.bbox_right, tot_gate_obj.bbox_bottom, minus_icon, "minus_icon")
        negotiation_planes = []
        for i in range(300 + minus_icon.width, 14 * 30 + 300 + minus_icon.width, 30):
            negotiation_planes.append(Hud_Obj(i, tot_gate_obj.bbox_bottom, flight_sprite, "plane" + str(i), visible=False))
        plus_icon = sge.gfx.Sprite("plus_icon", global_values.graphics_directory)
        plus_icon_obj = Hud_Obj(negotiation_planes[13].bbox_right + 20, tot_gate_obj.bbox_bottom, plus_icon, "plus_icon")
        gate_num = sge.gfx.Sprite(width=60, height=30)
        gate_num_obj = Hud_Obj(plus_icon_obj.bbox_right + 20, tot_gate_obj.bbox_bottom, gate_num)
        submit_button = sge.gfx.Sprite("submit_arrow", global_values.graphics_directory)
        submit_button_obj = Hud_Obj(gate_num_obj.bbox_right + 20, tot_gate_obj.bbox_bottom, submit_button, obj_name="submit")
        neg_prompt = sge.gfx.Sprite(width=700, height=30)
        neg_prompt_obj = Hud_Obj(air_name_obj.bbox_right + 20, air_name_obj.bbox_top, neg_prompt, "neg_prompt")
        object_list.extend((neg_text_obj, gate_num_obj, submit_button_obj, minus_icon_obj, plus_icon_obj, neg_prompt_obj))
        object_list.extend(negotiation_planes)
        return negotiation_planes, gate_num_obj, neg_prompt_obj


def airport_graphics(old_height, city):
    total_gate_name = sge.gfx.Sprite(width=80, height=40)
    total_gates = sge.gfx.Sprite(width=80, height=80)
    first_airline = sge.gfx.Sprite(width=200, height=40)
    first_airline_gates = sge.gfx.Sprite(width=80, height=80)

    first_airline.draw_text(global_values.small_text_font, global_values.player.airline_name, 0, 0, color=global_values.text_color)
    first_airline_gates.draw_text(global_values.small_text_font,
                                  "{0}\n----\n{1}".format(city.airport.get_flights(global_values.player.airline_name), city.airport.get_gates(global_values.player.airline_name))
                                  , 0, 0, color=global_values.text_color)
    total_gate_name.draw_text(global_values.small_text_font, "Total", 0, 0, color=global_values.text_color)
    total_gates.draw_text(global_values.small_text_font, "{0}\n---\n{1}".format(city.airport.total_used, city.airport.total_gates), 0, 0 , color=global_values.text_color)

    total_gate_name_obj = Hud_Obj(0, old_height, sprite=total_gate_name, obj_name="total_gate_name")
    total_gates_obj = Hud_Obj(0, total_gate_name_obj.bbox_bottom, sprite=total_gates, obj_name="total_gates")
    first_airline_name_obj = Hud_Obj(total_gate_name_obj.bbox_width + global_values.ICON_OFFSET, old_height, sprite=first_airline, obj_name="first_airline_name")
    first_airline_gates_obj = Hud_Obj(total_gate_name_obj.bbox_width + global_values.ICON_OFFSET, first_airline_name_obj.bbox_bottom, sprite=first_airline_gates, obj_name="first_airline_gates")

    return total_gate_name_obj, total_gates_obj, first_airline_name_obj, first_airline_gates_obj