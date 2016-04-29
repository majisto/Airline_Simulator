import os
import sge
import airline_manufacturer
import global_values

#Constants for sprite names.
boeing_sprite_name = 'boeing_manufacturer_icon'
airbus_sprite_name = 'airbus_manufacturer_icon'
tupolev_sprite_name = 'tupolev_manufacturer_icon'
map_sprite_name = 'cropped_us_europe'

class Manufacturer_Home (sge.dsp.Room):

    def event_room_start(self):
        self.name = self.__class__.__name__
        self.manufacturer_music = sge.snd.Music(os.path.join('music', 'manufacturer_home.ogg'))
        self.manufacturer_music.play()

    def event_room_end(self):
        self.manufacturer_music.stop()

    def event_key_press(self, key, char):
        if key == "b":
            sge.snd.Music.stop()
            global_values.room_dict["region"].start(transition="pixelate", transition_time=500)

    def event_room_resume(self):
        self.manufacturer_music.play()

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            Man_Room = airline_manufacturer.create_room(obj.sprite.name)
            global_values.room_dict["man_home"] = self
            self.manufacturer_music.stop()
            Man_Room.start(transition="iris_out", transition_time=500, transition_arg=(x_pos, y_pos))

def create_room():
    #Sprites
    background_map = sge.gfx.Sprite(map_sprite_name, global_values.graphics_directory)
    airbus_logo = sge.gfx.Sprite(airbus_sprite_name, global_values.graphics_directory)
    boeing_logo = sge.gfx.Sprite(boeing_sprite_name, global_values.graphics_directory)
    tupolev_logo = sge.gfx.Sprite(tupolev_sprite_name, global_values.graphics_directory)
    text_box = sge.gfx.Sprite(width=sge.game.width, height=100)
    airline_name = sge.gfx.Sprite(width=200, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)

    #Rectangles
    text_box.draw_rectangle(0,0, text_box.width - 5, text_box.height - 5, outline=sge.gfx.Color("gray")
        ,outline_thickness=5)

    #Font
    text_font = sge.gfx.Font("Droid Sans Mono", size=28)

    text_box.draw_text(text_font, "Which manufacturer would you like to visit?", 5, 5,
                       color=sge.gfx.Color("black"))
    airline_name.draw_text(text_font, global_values.player.airline_name, 0, 0, color=sge.gfx.Color("red"))
    airline_cash.draw_text(text_font, '${:0,}K'.format(global_values.player.money2), 0, 0, color=sge.gfx.Color("red"))

    boeing_object = sge.dsp.Object(20, 150, z=1, sprite=boeing_logo)
    airbus_object = sge.dsp.Object(580, 140, z=1, sprite=airbus_logo)
    tupolev_object = sge.dsp.Object(sge.game.width - tupolev_logo.width, 40, z=1, sprite=tupolev_logo)
    object_list = [boeing_object, airbus_object, tupolev_object]

    #Background Layer
    layers = [sge.gfx.BackgroundLayer(background_map, 0, 0, -10000),
              sge.gfx.BackgroundLayer(airline_name, 0, sge.game.height - airline_name.height, 1),
              sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width, sge.game.height - airline_name.height, 1),
              sge.gfx.BackgroundLayer(text_box, 0, 500, 1)]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return Manufacturer_Home(background=background, objects=object_list)