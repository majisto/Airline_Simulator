import sge
import global_values
import launch_room
import city

class Game(sge.dsp.Game):

    def event_close(self):
        self.end()


if __name__ == '__main__':
    Airline_Game = Game(width=800, height=600, fps=60, window_text="Airline_Simulator")
    global_values.game = Airline_Game
    global_values.text_font = sge.gfx.Font("Droid Sans Mono", size=28)
    city_dot = sge.gfx.Sprite(width=8, height=8)
    new_york = city.City("New York\nUnited States", (710, 210), "NA", 18, 60, 80, sprite=city_dot)
    Main_Room = city.create_city_room(new_york)
    sge.game.start_room = Main_Room
    Airline_Game.start()