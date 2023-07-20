VAL_DICT = {
    "Empty": 0,
    "Border": 1,
    "Path": 2,
    "Parking_slot": 3,
    "Robot": 4
}


class Car:
    def __init__(self, position=None, direction=None):
        self.position = position
        self.direction = direction

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction

    def set_position(self, new_position):
        self.position = new_position

    def set_direction(self, new_direction):
        self.direction = new_direction


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