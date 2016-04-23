import sge

import airline_manufacturer_home
import globally_stuff
import planes


class Game(sge.dsp.Game):

    def event_close(self):
        self.end()

    def event_key_press(self, key, char):
        if key == "s":
            print self.current_room.name

if __name__ == '__main__':
    Airline_Game = Game(width=800, height=600, fps=120, window_text="Airline_Simulator", grab_input=True)
    globally_stuff.game = Airline_Game
    globally_stuff.text_font = sge.gfx.Font("Droid Sans Mono", size=24)
    Main_Room = airline_manufacturer_home.create_room()
    globally_stuff.room_list.append(Main_Room)
    globally_stuff.plane_list = planes.get_plane_list()
    sge.game.start_room = Main_Room
    Airline_Game.start()