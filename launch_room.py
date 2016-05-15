import sge

import global_values
import planes
import player
import region_room

text_box = None
prompt = None

class Launch_Room(sge.dsp.Room):

    airline_name = []

    def event_room_start(self):
        prompt.draw_text(global_values.text_font, "Please name your airline below.  Max 13 characters.", 0, 0, color=sge.gfx.Color('black'))

    def event_key_press(self, key, char):
        if len(self.airline_name) > 14 and key != "backspace":
            return
        if key == "backspace":
            if len(self.airline_name) > 0:
                del (self.airline_name[-1])
                text_box.draw_clear()
                text_box.draw_rectangle(0, 0, text_box.width - 5, text_box.height - 5, outline=sge.gfx.Color("gray")
                                        , outline_thickness=5)
                text_box.draw_text(global_values.text_font, ''.join(self.airline_name), 5, 5, color=sge.gfx.Color('black'))
            return
        elif key == "enter":
            p = player.Player("1,000,000K", ''.join(self.airline_name), 1000000)
            p.hubs["NA"] = "austxus"
            global_values.player = p
            Main_Room = region_room.create_room()
            Main_Room.region_name = "NA"
            global_values.room_list.append(Main_Room)
            global_values.room_dict["region"] = Main_Room
            global_values.plane_list = planes.get_plane_list()
            p.hangar["b7878"] = 2
            p.hangar["b737100"] = 2
            Main_Room.start()
        self.airline_name.append(char)
        text_box.draw_rectangle(0, 0, text_box.width - 5, text_box.height - 5, outline=sge.gfx.Color("gray")
                                , outline_thickness=5)
        text_box.draw_text(global_values.text_font, ''.join(self.airline_name), 5, 5, color=sge.gfx.Color('black'))

def create_room():
    global text_box, prompt
    text_box = sge.gfx.Sprite(width=sge.game.width, height=50)
    text_box.draw_rectangle(0, 0, text_box.width - 5, text_box.height - 5, outline=sge.gfx.Color("gray")
                            , outline_thickness=5)
    prompt = sge.gfx.Sprite(width=sge.game.width, height=50)
    airline_select_object = sge.dsp.Object(0, 0, z=1, sprite=prompt)
    text_box_object = sge.dsp.Object(0, 50, z=1, sprite=text_box)
    lay = []
    object_list = [text_box_object, airline_select_object]
    background_manufacturer = sge.gfx.Background(lay, sge.gfx.Color("white"))
    return Launch_Room(background=background_manufacturer, objects=object_list)