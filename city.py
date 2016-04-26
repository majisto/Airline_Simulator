import sge
import global_values

POP_ICON = 'population_icon'
ECON_ICON = 'economy_icon_cropped'

class City(sge.dsp.Object):

    def __init__(self, name, coordinates, region, population, tourism, economy, sprite):
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

    def event_room_start(self):
        for obj in self.objects:
            if type(obj) == sge.dsp.Object:
                if obj.name == "pop":
                    obj.sprite.draw_clear()
                    obj.sprite.draw_text(global_values.text_font, str(self.city.population) + "M", 0, 0,
                                         color=sge.gfx.Color("black"))
                elif obj.name == "econ":
                    obj.sprite.draw_text(global_values.text_font, str(self.city.economy), 0, 0,
                                         color=sge.gfx.Color("black"))
                elif obj.name == "city_name":
                    city_font = sge.gfx.Font("droid sans mono", size=40)
                    obj.sprite.draw_rectangle(0, 0, obj.sprite.width, obj.sprite.height ,
                                              outline=sge.gfx.Color("gray"), outline_thickness=5)
                    # obj.sprite.draw_text(city_font, self.city.city_name, 0,0,
                    #                      color=sge.gfx.Color("black"))
def create_city_room(City_Class):
    city_font = sge.gfx.Font("droid sans mono", size=40)
    #Sprites
    population_icon = sge.gfx.Sprite( POP_ICON, global_values.graphics_directory)
    economy_icon = sge.gfx.Sprite(ECON_ICON, global_values.graphics_directory)
    population_number = sge.gfx.Sprite(width=80, height=population_icon.height)
    economy_number = sge.gfx.Sprite(width=80, height=economy_icon.height)
    city_name = sge.gfx.Sprite(width=sge.game.width, height=90)
    city_name.draw_text(city_font, City_Class.city_name, 0,0, halign="center",
                                         color=sge.gfx.Color("black"))

    #Objects/Layers
    layers = [sge.gfx.BackgroundLayer(population_icon, 0, 100, -1000),
              sge.gfx.BackgroundLayer(economy_icon, population_number.width + population_icon.width, 100, -1000)]
    population_number_object = sge.dsp.Object(population_icon.width, 100, z=1, sprite=population_number)
    population_number_object.name = "pop"
    economy_number_object = sge.dsp.Object(economy_icon.width + population_icon.width + population_number_object.bbox_width,
                                           100, z=1, sprite=economy_number)
    economy_number_object.name = "econ"
    city_name_object = sge.dsp.Object(0, 0, z=10, sprite=city_name)
    city_name_object.name = "city_name"

    object_list = [population_number_object, economy_number_object, city_name_object]
    background = sge.gfx.Background(layers, sge.gfx.Color("white"))
    return City_Room(City_Class, background=background, objects=object_list)