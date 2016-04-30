import sge
from interactive_obj import I_Obj
import airline_manufacturer_home
import city
import global_values

map_sprite_name = 'usa_canada_islands'
class Region_Room(sge.dsp.Room):

    def event_room_start(self):
        pass

    def event_key_press(self, key, char):
        pass

    def event_room_resume(self):
        self.background.layers[2].sprite.draw_clear()
        self.background.layers[2].sprite.draw_text(global_values.text_font,
                                                   '${:0,}K'.format(global_values.player.money2)
                                                   , 0, 10, color=sge.gfx.Color("red"))

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            obj_name = obj.get_name()
            if obj_name == "city":
                City_Room = city.create_city_room(obj)
                City_Room.start(transition="pixelate", transition_time=500)
            elif obj_name == "factory":
                Next_Room = airline_manufacturer_home.create_room()
                global_values.room_list.append(Next_Room)
                Next_Room.start(transition="pixelate", transition_time=500)
            elif obj_name == "ticket":
                print "New Route WIP"

def create_room():
    # Sprites
    city_dot = sge.gfx.Sprite(width=8,height=8)
    austin_dot = sge.gfx.Sprite(width=8,height=8)
    airline_name = sge.gfx.Sprite(width=250, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)
    cash_font = sge.gfx.Font("droid sans mono", size=30)
    factory = sge.gfx.Sprite("factory_cropped", global_values.graphics_directory)
    ticket = sge.gfx.Sprite("ticket_cropped", global_values.graphics_directory)

    background_map = sge.gfx.Sprite(map_sprite_name, global_values.graphics_directory)

    airline_name.draw_text(cash_font, global_values.player.airline_name, 0, 10, color=sge.gfx.Color("red"))
    airline_cash.draw_text(cash_font, '${:0,}K'.format(global_values.player.money2), 0, 10, color=sge.gfx.Color("red"),
                           halign='left')
    city_dot.draw_ellipse(0, 0, city_dot.width, city_dot.height, fill=sge.gfx.Color("green"))
    austin_dot.draw_ellipse(0, 0, austin_dot.width, austin_dot.height, fill=sge.gfx.Color("green"))
    name_layer = sge.gfx.BackgroundLayer(airline_name, 0, background_map.height, 1)
    factory_object = I_Obj(name_layer.x + name_layer.sprite.width, name_layer.y, sprite=factory, obj_name="factory")
    ticket_object = I_Obj(factory_object.x + factory_object.bbox_width + global_values.ICON_OFFSET,
                          factory_object.y, sprite=ticket, obj_name="ticket")

    austin = city.City("Austin, TX\nUnited States", (420, 392), "NA", 2, 65, 85, sprite=city_dot)
    new_york = city.City("New York, NY\nUnited States", (742, 186), "NA", 18, 60,80, sprite=austin_dot)

    object_list = [new_york, austin, factory_object, ticket_object]
    layers = [sge.gfx.BackgroundLayer(background_map, 0, 0, -1000), name_layer,
              sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width,
                                      background_map.height, 1)]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Region_Room(background=background, objects=object_list)