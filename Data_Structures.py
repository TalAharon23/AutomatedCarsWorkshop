
import threading

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
x_parking_delta = 65
y_parking_delta = 150


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
ds_mutex = threading.Lock()


class Val_dict:
    EMPTY = 0
    BORDER = 1
    PARKING_SLOT = 2
    CAR = 3
    BFS_ROAD = 4


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Cell:
    def __init__(self, x, y, dist=None, prev=None):
        self.x = x
        self.y = y
        self.dist = dist  # distance to start
        self.prev = prev  # parent cell in the path

    def X(self):
        return self.x

    def Y(self):
        return self.y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Car:
    def __init__(self, position=None, direction_degrees=None, next_Step=None):
        self.position = position
        self.direction_degrees = direction_degrees
        self.next_step = next_Step

    def get_position(self):
        ds_mutex.acquire()
        temp = self.position
        ds_mutex.release()
        return temp

    def get_direction_degrees(self):
        ds_mutex.acquire()
        temp = self.direction_degrees
        ds_mutex.release()
        return temp

    def set_position(self, new_position: Cell):
        ds_mutex.acquire()
        self.position = new_position
        ds_mutex.release()

    def set_direction_degrees(self, new_direction):
        ds_mutex.acquire()
        self.direction_degrees = new_direction
        ds_mutex.release()


class Parking_Slots(metaclass=Singleton):
    def __init__(self, position=None, direction=None):
        self.parking_slots = []
        self.parking_slots_contours = []
        self.parking_angles = []

    def get_parking_slots(self):
        ds_mutex.acquire()
        temp = self.parking_slots.copy()
        ds_mutex.release()
        return temp

    def get_parking_angles(self):
        ds_mutex.acquire()
        temp = self.parking_angles.copy()
        ds_mutex.release()
        return temp

    def get_parking_slots_contours(self):
        ds_mutex.acquire()
        temp = self.parking_slots_contours.copy()
        ds_mutex.release()
        return temp

    def clean_parking_slots(self):
        ds_mutex.acquire()
        self.parking_slots.clear()
        ds_mutex.release()

    def clean_parking_slots_contours(self):
        ds_mutex.acquire()
        self.parking_slots_contours.clear()
        ds_mutex.release()

    def remove_slot(self, slot):
        ds_mutex.acquire()
        self.parking_slots.remove(slot)
        ds_mutex.release()

    def save_slot(self, slot, angle):
        ds_mutex.acquire()
        self.parking_slots.append(slot)
        self.parking_angles.append(angle)
        ds_mutex.release()

    def save_slot_contours(self, slot):
        ds_mutex.acquire()
        self.parking_slots_contours.append(slot)
        ds_mutex.release()


class contour_data:
    def __init__(self, width, length, color_name, rice):
        self.width = width
        self.length = length
        self.color_name = color_name
        self.rice = rice
