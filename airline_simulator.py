import sge

import global_values
import launch_room
import city
import routes

class Game(sge.dsp.Game):

    def event_close(self):
        self.end()


if __name__ == '__main__':
    Airline_Game = Game(width=1000, height=700, fps=60, window_text="Airline_Simulator")
    global_values.game = Airline_Game
    global_values.text_font = sge.gfx.Font("Droid Sans Mono", size=28)
    global_values.small_text_font = sge.gfx.Font('droid sans mono', size=20)
    global_values.text_color = sge.gfx.Color("black")
    Main_Room = launch_room.create_room()
    sge.game.start_room = Main_Room
    city.create_cities()
    Airline_Game.start()