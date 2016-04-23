import sge
import airline_manufacturer_home
import planes
import globally_stuff

class Game(sge.dsp.Game):

    def event_close(self):
        self.end()

    def event_key_press(self, key, char):
        if key == "s":
            print self.current_room.name

plane_list = planes.get_plane_list()

if __name__ == '__main__':
    Room_list = []
    Airline_Game = Game(width=800, height=600, fps=120, window_text="Airline_Simulator", grab_input=True)
    globally_stuff.game = Airline_Game
    Main_Room = airline_manufacturer_home.create_room()
    Room_list.append(Main_Room)
    globally_stuff.room_list = Room_list
    globally_stuff.plane_list = plane_list
    sge.game.start_room = Main_Room
    Airline_Game.start()