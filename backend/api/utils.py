from math import sin, cos, sqrt, atan2, radians


def coords_distance(lat1, long1, lat2, long2):
    """
    Calcula a distancia em kilometros entre duas coordenadas.
    """
    # Raio aproximado da terra
    R = 6373.0

    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)

    dlong = long2 - long1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
