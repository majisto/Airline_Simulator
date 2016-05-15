import os

debug = True
room_list = [] #All active rooms
city_list = [] #All Cities
city_dict = {} #Cities by region
room_dict = {}
city_shortname_dict = {}
plane_list = [] #All list_of_planes possible
manufacturer_dict = {} #Key: Manufacturer, Value: List of list_of_planes under manufacturer
plane_shortname_dict = {} #Maps plane shortnames to plane objects
manufacturer_list = set()
game = None #Game Object
text_font = None
cash_font = None
text_color = None
small_text_font = None
player = None
graphics_directory = os.path.join(os.path.dirname(__file__), 'graphics')
music_directory = os.path.join(os.path.dirname(__file__), "music")
planes_directory = os.path.join(graphics_directory, "planes")
boeing_sprite_name = 'boeing_manufacturer_icon'
airbus_sprite_name = 'airbus_manufacturer_icon'
tupolev_sprite_name = 'tupolev_manufacturer_icon'
ICON_OFFSET = 20