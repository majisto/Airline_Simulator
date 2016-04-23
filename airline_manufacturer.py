import sge
import globally_stuff

class Manufacturer(sge.dsp.Room):

    def __init__(self, selected_manufacturer, background):
        super(Manufacturer, self).__init__(background=background)
        self.plane_list = selected_manufacturer

    def event_room_start(self):
        pass

    def event_mouse_button_press(self, button):
        print ("X position in Man: {0}".format(sge.mouse.get_x()))
        print ("Y position in Man: {0}".format(sge.mouse.get_y()))
        for a in self.plane_list:
            print vars(a)
        print globally_stuff.room_list