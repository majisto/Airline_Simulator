import csv
import os
import sge
import global_values

plane_list = []
manufacturer_list = set()

class Airplane:
    def __init__(self, l):
        l[0] = l[0].strip()
        self.manufacturer = l[0]
        self.model = l[1]
        self.variant = l[2]
        self.first_flight = l[3]
        self.distance = l[4]
        self.fuel_efficiency = l[5]
        self.maintenance = l[6]
        self.seats = l[7]
        self.short_name = l[8]
        self.cost = l[9]
        directory_name = os.path.join(global_values.planes_directory, l[0])
        self.plane_sprite = sge.gfx.Sprite(l[10], directory_name)
        self.description = l[11]
        self.production = True

def get_plane_list():
    if plane_list is None or len(plane_list) == 0:
        with open("Airplane_Master_List.csv", "r") as f:
            airplanes = csv.reader(f, delimiter=',', quotechar='|')
            for plane in airplanes:
                assert isinstance(plane, list) and len(plane) == 12
                a = Airplane(plane)
                manufacturer_list.add(a.manufacturer)
                plane_list.append(a)
                if a.manufacturer in global_values.manufacturer_dict:
                    global_values.manufacturer_dict[a.manufacturer].append(a)
                else:
                    global_values.manufacturer_dict[a.manufacturer] = [a]
                global_values.plane_shortname_dict[a.short_name] = a
    return plane_list

if __name__ == '__main__':
    pass
