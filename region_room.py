import os

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

    def event_key_press(self, key, char):
        if char == "s":
            for obj in self.objects:
                if type(obj) == I_Obj:
                    if obj.get_name() == "ticket":
                        obj.sprite.draw_rectangle(0, 0, obj.sprite.width, obj.sprite.height, outline=sge.gfx.Color("white"),
                              outline_thickness=3)
                        self.new_route_on = False
        if char == "h":
            print (global_values.player.hangar)

    def event_room_resume(self):
        if not self.music.playing:
            self.music.play(loops=0)
        self.update_cash_display()
        for route in global_values.player.route_list:
            for obj in self.objects:
                if type(obj) == I_Obj and obj.obj_name == "map":
                    obj.sprite.draw_line(x1=route.city1.x + 5, y1= route.city1.y + 5, x2= route.city2.x + 5, y2=route.city2.y + 5,
                                         color=global_values.text_color, thickness=1)

    def update_cash_display(self):
        self.background.layers[1].sprite.draw_clear()
        self.background.layers[1].sprite.draw_text(global_values.text_font,
                                                   '${:0,}K'.format(global_values.player.money2)
                                                   , 0, 10, color=sge.gfx.Color("red"))

    def check_route_exists(self, dest_city):
        for rt in global_values.player.route_list:
            if dest_city.shortname in [rt.city1.shortname, rt.city2.shortname]:
                return True
        return False

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            obj_name = obj.get_name()
            if obj_name == "city":
                if not self.new_route_on:
                    City_Room = city.create_city_room(obj)
                    City_Room.start(transition="pixelate", transition_time=500)
                else:
                    if self.check_route_exists(obj):
                        return
                    route_prompt_global.sprite.draw_clear()
                    ticket_global.sprite.draw_rectangle(0, 0, ticket_global.sprite.width, ticket_global.sprite.height,
                                                        outline=sge.gfx.Color("white"), outline_thickness=3)
                    try:
                        Route_Room = routes.create_room(self.get_hub_city(), obj)
                    except ValueError:
                        return
                    Route_Room.start()
            elif obj_name == "factory":
                Next_Room = airline_manufacturer_home.create_room()
                global_values.room_list.append(Next_Room)
                Next_Room.start(transition="pixelate", transition_time=500)
            elif obj_name == "ticket":
                obj.sprite.draw_rectangle(0, 0, obj.sprite.width, obj.sprite.height, outline=sge.gfx.Color("blue"),
                                          outline_thickness=3)
                route_prompt_global.sprite.draw_text(global_values.small_text_font,
                        "Route starts from {0}.  Please select a destination.".format(self.get_hub_city().name_no_country), 0, 0, color=sge.gfx.Color("black"))
                self.new_route_on = True
            elif obj_name == "end":
                calculate_profit()
                self.update_cash_display()
    def get_hub_city(self):
        assert "region_name" in vars(self)
        return global_values.city_shortname_dict[global_values.player.hubs[self.region_name]]

def create_room():
    global route_prompt_global
    global ticket_global
    # Sprites
    airline_name = sge.gfx.Sprite(width=250, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)
    cash_font = sge.gfx.Font("droid sans mono", size=30)
    factory = sge.gfx.Sprite("factory_cropped", global_values.graphics_directory)
    ticket = sge.gfx.Sprite("ticket_cropped", global_values.graphics_directory)
    end_turn = sge.gfx.Sprite("end_button", global_values.graphics_directory)
    background_map = sge.gfx.Sprite(map_sprite_name, global_values.graphics_directory)
    prompt = sge.gfx.Sprite(width=750, height=50)

    airline_name.draw_text(cash_font, global_values.player.airline_name, 0, 10, color=sge.gfx.Color("red"))
    airline_cash.draw_text(cash_font, '${:0,}K'.format(global_values.player.money2), 0, 10, color=sge.gfx.Color("red"),
                           halign='left')

    name_layer = sge.gfx.BackgroundLayer(airline_name, 0, background_map.height, 1)
    factory_object = I_Obj(name_layer.x + name_layer.sprite.width, name_layer.y, sprite=factory, obj_name="factory")
    ticket_object = I_Obj(factory_object.x + factory_object.bbox_width + global_values.ICON_OFFSET,
                          factory_object.y, sprite=ticket, obj_name="ticket")
    end_turn_object = I_Obj(ticket_object.x + ticket_object.bbox_width + global_values.ICON_OFFSET, factory_object.y,
                            sprite=end_turn, obj_name="end")
    prompt_object = I_Obj(200, sge.game.height - airline_name.height - prompt.height,
                          sprite=prompt, obj_name="prompt", z=2)
    route_prompt_global = prompt_object
    ticket_global = ticket_object
    map_object = I_Obj(0, 0, sprite=background_map, obj_name="map", z=-10)
    object_list = get_cities()
    object_list.extend((factory_object, ticket_object, prompt_object, map_object, end_turn_object))
    layers = [name_layer,
              sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width,
                                      background_map.height, 1)]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Region_Room(background=background, objects=object_list)

def calculate_profit():
    for route in global_values.player.route_list:
        total_seats = int(route.plane.seats) * route.num_planes
        total_passengers = int(routes.calculate_total_passengers(route.city1, route.city2))
        if total_passengers >= total_seats:
            sales = route.fare * total_seats
        else:
            sales = route.fare * (total_seats - total_passengers)
        global_values.player.money2 += sales
        if global_values.debug:
            print ("Total sales is {0} on route to {1}".format(sales, route.city2.name_no_country))

def get_cities():
    o_list = []
    for local_city in global_values.city_list:
        o_list.append(local_city)
    return o_list