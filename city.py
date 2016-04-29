import sge
import global_values

POP_ICON_FILENAME = 'population_icon'
ECON_ICON_FILENAME = 'economy_icon_cropped'


class City(sge.dsp.Object):

    def __init__(self, name, coordinates, region, population, tourism, economy, sprite=None):
        super(City, self).__init__(x=coordinates[0], y=coordinates[1], sprite=sprite)
        self.economy = economy
        self.tourism = tourism
        self.population = population
        self.region = region
        self.city_name = name
    pass

class City_Room(sge.dsp.Room):

    def __init__(self, City_Class, background, objects):
        super(City_Room, self).__init__(background=background, objects=objects)
        self.city = City_Class

    def event_key_press(self, key, char):
        if key == "b":
            global_values.room_dict["region"].start(transition="pixelate", transition_time=500)

    def event_room_start(self):
        for obj in self.objects:
            if type(obj) == sge.dsp.Object:
                if obj.name == "pop":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.population) + "M", 0, 0,
                                         color=sge.gfx.Color("black"))
                elif obj.name == "econ":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.economy), 0, 0,
                                         color=sge.gfx.Color("black"))
                elif obj.name == "city_name":
                    obj.sprite.draw_clear()
                    city_font = sge.gfx.Font("droid sans mono", size=40)
                    obj.sprite.draw_rectangle(0, 0, obj.sprite.width, obj.sprite.height ,
                                              outline=sge.gfx.Color("gray"), outline_thickness=2)
                    obj.sprite.draw_text(city_font, self.city.city_name, global_values.game.width / 3,0,
                                         color=sge.gfx.Color("black"))
                elif obj.name == "tour":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.tourism), 0, 0,
                                         color=sge.gfx.Color("black"))
def create_city_room(City_Class):
    POP_ICON_POSITION = (0, 100)
    ECON_ICON_POSITION = (sge.game.width / 4, 100)
    TOURISM_ICON_POSITION = (sge.game.width / 2, 100)

    #Sprites
    population_icon = sge.gfx.Sprite(POP_ICON_FILENAME, global_values.graphics_directory)
    economy_icon = sge.gfx.Sprite(ECON_ICON_FILENAME, global_values.graphics_directory)
    tourism_icon = sge.gfx.Sprite("tourism_cropped", global_values.graphics_directory)
    country_flag = sge.gfx.Sprite("us_flag_cropped", global_values.graphics_directory + "/flags", transparent=False)
    population_number = sge.gfx.Sprite(width=80, height=population_icon.height)
    economy_number = sge.gfx.Sprite(width=60, height=economy_icon.height)
    tourism_number = sge.gfx.Sprite(width=60, height=tourism_icon.height)
    city_name = sge.gfx.Sprite(width=sge.game.width, height=90)
    relation = sge.gfx.Sprite("hand_shake_cropped", global_values.graphics_directory)
    airline_name = sge.gfx.Sprite(width=200, height=50)
    airline_cash = sge.gfx.Sprite(width=200, height=50)

    airline_name.draw_text(global_values.text_font, global_values.player.airline_name, 0, 0, color=sge.gfx.Color("red"))
    airline_cash.draw_text(global_values.text_font, '${:0,}K'.format(global_values.player.money2), 0, 0,
                           color=sge.gfx.Color("red"),
                           halign='left')

    #Objects/Layers
    layers = [sge.gfx.BackgroundLayer(population_icon, POP_ICON_POSITION[0], POP_ICON_POSITION[1], -1000),
              sge.gfx.BackgroundLayer(economy_icon, ECON_ICON_POSITION[0], 100, -1000),
              sge.gfx.BackgroundLayer(tourism_icon, TOURISM_ICON_POSITION[0], 100, -1000),
              sge.gfx.BackgroundLayer(airline_name, 0, sge.game.height - airline_name.height),
              sge.gfx.BackgroundLayer(airline_cash, sge.game.width - airline_cash.width, sge.game.height - airline_name.height)]
    population_number_object = sge.dsp.Object(population_icon.width + 50, 100, z=1, sprite=population_number)
    population_number_object.name = "pop"
    economy_number_object = sge.dsp.Object(ECON_ICON_POSITION[0] + economy_icon.width + 50,
                                           100, z=1, sprite=economy_number)
    economy_number_object.name = "econ"
    city_name_object = sge.dsp.Object(0, 0, z=10, sprite=city_name)
    city_name_object.name = "city_name"
    flag_object = sge.dsp.Object(0,0, z=11, sprite=country_flag)
    flag_object.name = "flag"
    # tourism_object = sge.dsp.Object(economy_number_object.x + economy_number_object.bbox_width + 50, economy_number_object.y, sprite=tourism_icon)
    # tourism_object.name = "tourism"
    relation_object = sge.dsp.Object(global_values.game.width - 100,0, z=11, sprite=relation)
    relation_object.name = "relation"
    tourism_number_object = sge.dsp.Object(TOURISM_ICON_POSITION[0] + tourism_icon.width + 50, 100
                                           ,sprite=tourism_number)
    tourism_number_object.name = "tour"

    #Bottom Bar Area Objects


    object_list = [population_number_object, economy_number_object, city_name_object, flag_object,
                   relation_object, tourism_number_object]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return City_Room(City_Class, background=background, objects=object_list)