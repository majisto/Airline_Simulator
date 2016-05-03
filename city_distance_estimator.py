"""Uses the Haversine Formula recommended for calculating short
distances by NASA's Jet Propulsion Laboratory.  For longer
distances this formula tends to overestimate trans-polar distances and
underestimate trans-equatorial distances.
tested with Python27 and Python34  by  vegaseat  19jan2015
"""

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    calculate the great circle distance between two points
    on the Earth (coordinates specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # 6367 kilos (3961 miles) is the radius of the Earth
    kilos = 6367 * c
    miles = 3961 * c
    return kilos, miles

# km, miles = haversine(lon1, lat1, lon2, lat2)
# sf = "The distance between {} and {} is {:0.1f} miles (air)"
# print(sf.format(city1, city2, miles))