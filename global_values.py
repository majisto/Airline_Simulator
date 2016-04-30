import os
room_list = [] #All active rooms
room_dict = {}
plane_list = [] #All planes possible
manufacturer_dict = {} #Key: Manufacturer, Value: List of planes under manufacturer
plane_shortname_dict = {} #Maps plane shortnames to plane objects
manufacturer_list = set()
game = None #Game Object
text_font = None
player = None
graphics_directory = os.path.join(os.path.dirname(__file__), 'graphics')
music_directory = os.path.join(os.path.dirname(__file__), "music")
planes_directory = os.path.join(graphics_directory, "planes")
boeing_sprite_name = 'boeing_manufacturer_icon'
airbus_sprite_name = 'airbus_manufacturer_icon'
tupolev_sprite_name = 'tupolev_manufacturer_icon'
ICON_OFFSET = 20