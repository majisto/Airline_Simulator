import os

import sge

import airline_manufacturer_home
import globally_stuff

text_box = None

class Manufacturer(sge.dsp.Room):

    def __init__(self, selected_manufacturer, background, objects):
        super(Manufacturer, self).__init__(background=background, objects=objects)
        self.manufacturer = selected_manufacturer
        self.name = selected_manufacturer
        if self.manufacturer == airline_manufacturer_home.boeing_sprite_name:
            self.music = sge.snd.Music(os.path.join('music', 'mitsub_boeing.ogg'))
        elif self.manufacturer == airline_manufacturer_home.airbus_sprite_name:
            self.music = sge.snd.Music(os.path.join('music', 'nissan_airbus.ogg'))
        elif self.manufacturer == airline_manufacturer_home.tupolev_sprite_name:
            self.music = sge.snd.Music(os.path.join('music', 'mazda_tupolev.ogg'))

    def event_room_start(self):
        text_box.draw_text(globally_stuff.text_font, self.manufacturer, 5, 5, color=sge.gfx.Color("black"))
        print self.manufacturer
        print globally_stuff.room_list
        self.music.play()

    def event_room_end(self):
        self.music.stop(fade_time=500)

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            if obj.sprite.name == "back_button":
                for room in globally_stuff.room_list:
                    if isinstance(room, airline_manufacturer_home.Manufacturer_Home):
                        self.music.stop()
                        room.start(transition="iris_in", transition_time=500,transition_arg=(x_pos,y_pos))

def create_room(manufacturer):
    global text_box
    text_box = sge.gfx.Sprite(width=sge.game.width, height=150)
    back_button_icon = sge.gfx.Sprite("back_button", directory="graphics")
    text_box.my_name = "manufacturer_text_box"
    back_button_object = sge.dsp.Object(0,0, sprite=back_button_icon)
    text_box_object = sge.dsp.Object(0, 200, z=1, sprite=text_box)
    object_list = [text_box_object, back_button_object]
    lay = []
    background_manufacturer = sge.gfx.Background(lay, sge.gfx.Color("white"))
    return Manufacturer(selected_manufacturer=manufacturer, background=background_manufacturer,
                        objects=object_list)