# VAL_DICT = {
#     "Empty": 0,
#     "Border": 1,
#     "Path": 2,
#     "Parking_slot": 3,
#     "Robot": 4
# }

DIRECTION_DICT = {
    "NORTH": 0,
    "NORTH_EAST": 1,
    "EAST": 2,
    "EAST_SOUTH": 3,
    "SOUTH": 4,
    "SOUTH_WEST": 5,
    "WEST": 6,
    "WEST_NORTH": 7
}

class Val_dict:
    EMPTY           = 0
    BORDER          = 1
    PARKING_SLOT    = 2
    Car             = 3


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Car:
    def __init__(self, position=None, direction=None, next_Step=None):
        self.position               = position
        self.direction              = direction
        self.next_step              = next_Step

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction

    def set_position(self, new_position):
        self.position = new_position

    def set_direction(self, new_direction):
        self.direction = new_direction


class Parking_Slots(metaclass=Singleton):
    def __init__(self, position=None, direction=None):
        self.parking_slots = []

    def get_parking_solts(self):
        return self.parking_slots

    def clean_parking_solts(self):
        self.parking_slots.clear()

    def remove_slot(self, slot):
        self.parking_slots.remove(slot)

    def save_slot(self, slot):
        self.parking_slots.append(slot)


class Cell:
    def __init__(self, x, y, dist, prev):
        self.x = x
        self.y = y
        self.dist = dist;  # distance to start
        self.prev = prev;  # parent cell in the path

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class contour_data:
    def __init__(self, width, length, color_name, rice):
        self.width = width
        self.length = length
        self.color_name = color_name
        self.rice = rice