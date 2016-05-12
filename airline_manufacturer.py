import os
from itertools import cycle
import locale
import sge
import airline_manufacturer_home
import global_values
import planes

OFFSET_ICON = 30

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
        self.plane_list = global_values.manufacturer_dict[check_manufacturer(selected_manufacturer)[0]]
        self.cycler = cycle(self.plane_list)
        self.current_plane = None

    def event_room_start(self):
        self.music.play()
        self.current_plane = next(self.cycler)
        self.Loop_Objects(self.current_plane)

    def Loop_Objects(self, plane):
        city_font = sge.gfx.Font("droid sans mono", size=48)
        desc_font = sge.gfx.Font('droid sans mono', size=20)
        assert isinstance(plane, planes.Airplane)
        for obj in self.objects:
            if "name" in vars(obj) and type(obj) == sge.dsp.Object:
                if obj.name == "range":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(city_font, str(plane.distance) + " mi", 0, 0, color=sge.gfx.Color("black"))
                if obj.name == "name":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(city_font, "{0}-{1} ({2})".format(plane.model, plane.variant, plane.first_flight), 0, 0,
                                         color=sge.gfx.Color("black"))
                if obj.name == "picture":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_sprite(plane.plane_sprite, 0, obj.sprite.origin_x, obj.sprite.origin_y)
                if obj.name == "description":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(desc_font, plane.description, 0, 0,
                                         color=sge.gfx.Color("black"), width=sge.game.width)
                if obj.name == "fuel":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(city_font, plane.fuel_efficiency, 0, 0,
                         color=sge.gfx.Color("black"), width=sge.game.width)
                if obj.name == "maintenance":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(city_font, plane.maintenance, 0, 0,
                         color=sge.gfx.Color("black"), width=sge.game.width)
                if obj.name == "seating":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(city_font, plane.seats, 0, 0,
                         color=sge.gfx.Color("black"), width=sge.game.width)
                if obj.name == "cost":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(city_font, '${:0,}K'.format((plane.cost * 1000)), 0, 0,
                                         color=sge.gfx.Color("black"), width=sge.game.width)
    def event_room_end(self):
        self.music.stop(fade_time=500)

    def event_mouse_button_press(self, button):
        x_pos = sge.mouse.get_x()
        y_pos = sge.mouse.get_y()
        collied_objects = sge.collision.rectangle(x_pos, y_pos, 0, 0)
        for obj in collied_objects:
            if obj.name == "buy":
                if (int(self.current_plane.cost) * 1000) > global_values.player.money2:
                    return
                global_values.player.money2 -= int(self.current_plane.cost) * 1000
                if self.current_plane.short_name in global_values.player.hangar:
                    global_values.player.hangar[self.current_plane.short_name] += 1
                else:
                    global_values.player.hangar[self.current_plane.short_name] = 1
                for OBJ in self.objects:
                    if "name" in vars(OBJ) and type(OBJ) == sge.dsp.Object:
                        if OBJ.name == "cash":
                            OBJ.sprite.draw_clear()
                            OBJ.sprite.draw_text(global_values.text_font,
                                '${:0,}K'.format(global_values.player.money2), 0, 0, color=sge.gfx.Color("red"))

    def event_key_press(self, key, char):
        if key == "b":
            global_values.room_dict["man_home"].start()
        elif key == "right":
            self.current_plane = next(self.cycler)
            self.Loop_Objects(self.current_plane)
        elif key == "left":
            pass

def create_room(manufacturer):
    man_info = check_manufacturer(manufacturer)
    locale.setlocale(locale.LC_ALL, '')

    city_font = sge.gfx.Font("droid sans mono", size=40)

    text_box = sge.gfx.Sprite(width=sge.game.width, height=80)
    logo = sge.gfx.Sprite(man_info[1], global_values.graphics_directory)
    airplane_picture = sge.gfx.Sprite(width=600, height=474)
    airplane_name = sge.gfx.Sprite(width=sge.game.width - airplane_picture.width, height=50)
    range_icon = sge.gfx.Sprite("range", global_values.graphics_directory)
    range_number = sge.gfx.Sprite(width=sge.game.width - (range_icon.width + airplane_picture.width),
                                  height= range_icon.height)
    desc = sge.gfx.Sprite(width=sge.game.width, height=150)
    airline_name = sge.gfx.Sprite(width=200, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)
    fuel_icon = sge.gfx.Sprite("gas_pump_cropped", global_values.graphics_directory)
    fuel_icon_number = sge.gfx.Sprite(width=sge.game.width - (fuel_icon.width + airplane_picture.width),
                                  height= range_icon.height)
    maintenance_icon = sge.gfx.Sprite("wrench_cropped", global_values.graphics_directory)
    maintenance_number = sge.gfx.Sprite(width=sge.game.width, height=maintenance_icon.height)
    seating_icon = sge.gfx.Sprite("seatbelt_cropped", global_values.graphics_directory)
    seating_number = sge.gfx.Sprite(width=sge.game.width, height=seating_icon.height)
    cost_icon = sge.gfx.Sprite("wallet_cropped", global_values.graphics_directory)
    cost_number = sge.gfx.Sprite(width=sge.game.width, height=cost_icon.height)
    buy_button = sge.gfx.Sprite(width=sge.game.width - airplane_picture.width, height=50)

    buy_button.draw_rectangle(0, 0, buy_button.width, buy_button.height, outline=sge.gfx.Color("blue"),
                              outline_thickness=5)
    buy_button.draw_text(city_font, "Buy!", 160, 0, color=sge.gfx.Color("black"))
    text_box.draw_rectangle(0,0, text_box.width, text_box.height, outline=sge.gfx.Color("gray"),
                            outline_thickness=3)
    text_box.draw_text(city_font, man_info[0], 450, 15,
                       color=sge.gfx.Color("black"))
    airline_name.draw_text(global_values.text_font, global_values.player.airline_name, 0, 0, color=sge.gfx.Color("red"))
    airline_cash.draw_text(global_values.text_font, '${:0,}K'.format(global_values.player.money2), 0, 0, color=sge.gfx.Color("red"))

    text_box_object = sge.dsp.Object(0, 0, z=1, sprite=text_box)
    logo_object = sge.dsp.Object(0,0, z=2, sprite=logo)
    logo_object2 = sge.dsp.Object(sge.game.width - logo.width, 0, z=2, sprite=logo)
    airplane_name_object = sge.dsp.Object(airplane_picture.width, text_box.height, sprite=airplane_name)
    airplane_name_object.name = "name"
    range_number_object = sge.dsp.Object((range_icon.width + airplane_picture.width + OFFSET_ICON),
                                         text_box.height + airplane_name.height, z=2, sprite=range_number)
    range_number_object.name = "range"
    airplane_picture_object = sge.dsp.Object(0, text_box.height, z=2, sprite=airplane_picture)
    airplane_picture_object.name = "picture"
    desc_object = sge.dsp.Object(0, airplane_picture_object.bbox_bottom, sprite=desc)
    desc_object.name = "description"
    airline_cash_object = sge.dsp.Object(sge.game.width - airline_cash.width, sge.game.height - airline_name.height,
                                         sprite=airline_cash)
    airline_cash_object.name = "cash"
    fuel_icon_object = sge.dsp.Object(fuel_icon.width + airplane_picture.width + OFFSET_ICON,
                                      range_number_object.bbox_bottom, sprite=fuel_icon_number)
    fuel_icon_object.name = "fuel"
    maintenance_object = sge.dsp.Object(maintenance_icon.width + airplane_picture.width + OFFSET_ICON,
                                        fuel_icon_object.bbox_bottom, sprite=maintenance_number)
    maintenance_object.name = "maintenance"
    seating_number_object = sge.dsp.Object(seating_icon.width + airplane_picture.width + OFFSET_ICON,
                                           maintenance_object.bbox_bottom, sprite=seating_number)
    seating_number_object.name = "seating"
    cost_number_object = sge.dsp.Object(cost_icon.width + airplane_picture.width +OFFSET_ICON,
                                        seating_number_object.bbox_bottom, sprite=cost_number)
    cost_number_object.name = "cost"
    buy_button_object = sge.dsp.Object(airplane_picture.width, cost_number_object.bbox_bottom,sprite=buy_button)
    buy_button_object.name = "buy"

    object_list = [text_box_object, logo_object, logo_object2, airplane_picture_object,
                   range_number_object, airplane_name_object, desc_object, airline_cash_object,
                   fuel_icon_object, maintenance_object, seating_number_object, cost_number_object,
                   buy_button_object]
    lay = [sge.gfx.BackgroundLayer(range_icon, airplane_picture.width, range_number_object.y, 2),
           sge.gfx.BackgroundLayer(airline_name, 0, sge.game.height - airline_name.height, 1),
           sge.gfx.BackgroundLayer(fuel_icon, airplane_picture.width, fuel_icon_object.y),
           sge.gfx.BackgroundLayer(maintenance_icon, airplane_picture.width, maintenance_object.y),
           sge.gfx.BackgroundLayer(seating_icon, airplane_picture.width, seating_number_object.y),
           sge.gfx.BackgroundLayer(cost_icon, airplane_picture.width, cost_number_object.y)]
    background_manufacturer = sge.gfx.Background(lay, sge.gfx.Color("white"))
    return Manufacturer(selected_manufacturer=manufacturer, background=background_manufacturer,
                        objects=object_list)

def check_manufacturer(manufacturer):
    if manufacturer == global_values.boeing_sprite_name:
        return "Boeing", "boeing_logo_cropped"
    elif manufacturer == global_values.airbus_sprite_name:
        return "Airbus", "airbus_logo_square"
    elif manufacturer == global_values.tupolev_sprite_name:
        return "Tupolev", "Tupolev_logo_cropped"