import sge

import airline_manufacturer_home
import city
import globally_stuff

map_sprite_name = 'USA_blank_map'
class Region_Room(sge.dsp.Room):

    def event_room_start(self):
        pass
    def event_key_press(self, key, char):
        if key == "m":
            Next_Room = airline_manufacturer_home.create_room()
            globally_stuff.room_list.append(Next_Room)
            Next_Room.start(transition="pixelate", transition_time=500)

def create_room():
    # Sprites
    city_dot = sge.gfx.Sprite(width=8,height=8)
    airline_name = sge.gfx.Sprite(width=200, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)

    airline_name.draw_text(globally_stuff.text_font, globally_stuff.player.airline_name, 0, 0, color=sge.gfx.Color("red"))
    airline_cash.draw_text(globally_stuff.text_font, "${0}".format(globally_stuff.player.money), 0, 0, color=sge.gfx.Color("red"),
                           halign='left')
    city_dot.draw_ellipse(0, 0, city_dot.width, city_dot.height, fill=sge.gfx.Color("green"))
    new_york = city.City("New York", (710, 210), "NA", 18, 60,80, sprite=city_dot)
    background_map = sge.gfx.Sprite(map_sprite_name, globally_stuff.graphics_directory)
    object_list = [new_york]
    layers = [sge.gfx.BackgroundLayer(background_map, 0, 0, -1000),
              sge.gfx.BackgroundLayer(airline_name, 0, background_map.height, 1),
              sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width,
                                      background_map.height, 1)]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Region_Room(background=background, objects=object_list)