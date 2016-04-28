import os
import sge
import airline_manufacturer_home
import global_values

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
        self.music.play()

    def event_room_end(self):
        self.music.stop(fade_time=500)

    def event_key_press(self, key, char):
        if key == "b":
            global_values.room_dict["man_home"].start()

def create_room(manufacturer):
    global text_box
    man_info = check_manufacturer(manufacturer)
    city_font = sge.gfx.Font("droid sans mono", size=40)
    text_box = sge.gfx.Sprite(width=sge.game.width, height=80)
    logo = sge.gfx.Sprite(man_info[1], global_values.graphics_directory)
    text_box.my_name = "manufacturer_text_box"
    text_box.draw_rectangle(0,0, text_box.width, text_box.height, outline=sge.gfx.Color("gray"),
                            outline_thickness=3)
    text_box.draw_text(city_font, man_info[0], 350, 15,
                       color=sge.gfx.Color("black"))
    text_box_object = sge.dsp.Object(0, 0, z=1, sprite=text_box)
    logo_object = sge.dsp.Object(0,0, z=2, sprite=logo)
    logo_object2 = sge.dsp.Object(sge.game.width - logo.width, 0, z=2, sprite=logo)
    object_list = [text_box_object, logo_object, logo_object2]
    lay = []
    background_manufacturer = sge.gfx.Background(lay, sge.gfx.Color("white"))
    return Manufacturer(selected_manufacturer=manufacturer, background=background_manufacturer,
                        objects=object_list)

def check_manufacturer(manufacturer):
    if manufacturer == global_values.boeing_sprite_name:
        return "Boeing", "boeing_logo_cropped"
    elif manufacturer == global_values.airbus_sprite_name:
        return "Airbus", None
    elif manufacturer == global_values.tupolev_sprite_name:
        return "Tupolev", None