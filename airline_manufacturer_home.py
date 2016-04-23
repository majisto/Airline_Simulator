import os
import sge
import airline_manufacturer
import globally_stuff

class Manufacturer_Home (sge.dsp.Room):

    def event_room_start(self):
        self.name = self.__class__.__name__
        manufacturer_music = sge.snd.Music(os.path.join('music', 'airplane_manufacturer_select.ogg'))
        manufacturer_music.play()

    def event_key_press(self, key, char):
        pass

    def event_mouse_button_press(self, button):
        print ("Airline sim room list is {0}".format(globally_stuff.room_list))
        lay = []
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        print globally_stuff.game.window_text
        background_manufacturer = sge.gfx.Background(lay, sge.gfx.Color("white"))
        Man_Room = airline_manufacturer.Manufacturer(selected_manufacturer=globally_stuff.plane_list, background=background_manufacturer)
        globally_stuff.room_list.append(Man_Room)
        Man_Room.start(transition="iris_in")
        # if sge.mouse.get_x() > 20 and sge.mouse.get_y() > 20:
        #     sprite_list = []
        #     print ("Manufacturer Room created.")
        #     # Font
        #     text_font = sge.gfx.Font("Droid Sans Mono", size=24)
        #     p_list = planes.get_plane_list()
        #     for plane in p_list:
        #         # assert isinstance(plane, planes.Plane_Test)
        #         new_sprite = sge.gfx.Sprite(width=sge.game.width, height=30)
        #         new_sprite.draw_text(text_font, plane.manufacturer, 0, 0, color=sge.gfx.Color("red"), halign='left')
        #         sprite_list.append(new_sprite)
        #     layers_man = []
        #     i = 0
        #     for sp in sprite_list:
        #         layers_man.append(sge.gfx.BackgroundLayer(sp, 0, i, 1))
        #         i += sp.height
        #     background_manufacturer = sge.gfx.Background(layers_man, sge.gfx.Color("white"))
        #     Man_room = airline_manufacturer.Manufacturer(background=background_manufacturer)
        #     Man_room.p_list = p_list
        #     Man_room.start(transition="iris_in")
        pass

def create_room():
    #Sprites
    background_map = sge.gfx.Sprite('cropped_us_europe', 'graphics')
    airbus_logo = sge.gfx.Sprite('airbus_manufacturer_icon', 'graphics')
    boeing_logo = sge.gfx.Sprite('boeing_manufacturer_icon', 'graphics')
    tupolev_logo = sge.gfx.Sprite('tupolev_manufacturer_icon', 'graphics')
    text_box = sge.gfx.Sprite(width=sge.game.width, height=150)
    airline_name = sge.gfx.Sprite(width=150, height=50)
    airline_cash = sge.gfx.Sprite(width=160, height=50)

    #Rectangles
    text_box.draw_rectangle(0,0, text_box.width - 5, text_box.height - 5, outline=sge.gfx.Color("gray")
        ,outline_thickness=5)

    #Font
    text_font = sge.gfx.Font("Droid Sans Mono", size=24)
    # text_box.draw_clear()
    text_box.draw_text(text_font, "Which manufacturer would you like to visit?", 5, 5,
                       color=sge.gfx.Color("black"))
    airline_name.draw_text(text_font, "Metlink", 0, 0, color=sge.gfx.Color("red"))
    airline_cash.draw_text(text_font, "$2,500,000K ", 0, 0, color=sge.gfx.Color("red"), halign='left')

    #Background Layer
    layers = [sge.gfx.BackgroundLayer(background_map, 0, 0, -10000),
              sge.gfx.BackgroundLayer(boeing_logo, 20, 150, 1),
              sge.gfx.BackgroundLayer(airbus_logo, 580, 140, 1),
              sge.gfx.BackgroundLayer(tupolev_logo, sge.game.width - tupolev_logo.width, 40, 1),
              sge.gfx.BackgroundLayer(airline_name, 0, sge.game.height - airline_name.height, 1),
              sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width, sge.game.height - airline_name.height, 1),
              sge.gfx.BackgroundLayer(text_box, 0, 400, 1)]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Manufacturer_Home(background=background)