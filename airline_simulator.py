import sge
import global_values
import launch_room
import region_room


class Game(sge.dsp.Game):

    def event_close(self):
        self.end()


if __name__ == '__main__':
    Airline_Game = Game(width=800, height=600, fps=60, window_text="Airline_Simulator")
    global_values.game = Airline_Game
    global_values.text_font = sge.gfx.Font("Droid Sans Mono", size=20)
    Main_Room = launch_room.create_room()
    sge.game.start_room = Main_Room
    Airline_Game.start()