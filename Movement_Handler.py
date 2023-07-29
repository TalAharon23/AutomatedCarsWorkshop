from ESP32CAM_Car.Movement import move
from .Detection_Handler.Detection_controller import Detection_controller
import Data_Structures
import BFS_Logic

RIGHT_LEFT_DEGREE = 5

class MOVE_COMMANDS:
    Forward = "go"
    Left = "left"
    Right = "right"
    Back = "back"


class DIRECTIONS:
    Up = "Up"
    Left = "Left"
    Right = "Right"
    Down = "Down"

class Movement_Handler():

    def __init__(self):
        self.Detection_controller               = Detection_controller()
        self.BFS_Logic                          = BFS()
        self.car                                = Car()
        self.car_arrived_to_maneuver_point      = False
        self.car_arrived_to_destination         = False
        self.parking_slot_dest                  = None
        self.parking_slots                      = Parking_Slots()
        self.in_process                         = False

    def get_car_position(self):
        return self.car.get_position()

    def get_car_position_in_matrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == VAL_DICT["Robot"]:
                    return i, j
        raise ValueError("Matrix does not contain the car.")

    def get_in_process(self):
        return self.in_process

    def set_in_process(self, value):
        self.in_process = value

    def set_parking_slot_destination(self):
        chosen_slot = self.parking_slots[0]
        nearest_parking_slot_path = None
        dist_nearest_parking_slot = len(nearest_parking_slot_path)
        for slot in self.parking_slots:
            nearest_parking_slot_path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(), self.car.get_position(), self.slot)
            if len(nearest_parking_slot_path) < dist_nearest_parking_slot:
                dist_nearest_parking_slot = len(nearest_parking_slot_path)
                chosen_slot = slot

        self.parking_slot_dest = chosen_slot


    def car_movement(self, matrix):
        path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(), self.car.get_position(),
                                           self.parking_slot_dest)
        # understand the next cell
        # update car angle commands needed
        # move to the right angle
        # move forward for the next cell (maybe we will decide that can move few steps forward)



    def update_car_angle(self, car, next_direction):
        """
        :param car: object car for getting current angle of car
        :param next_direction: next direction in degrees (if right needed, it would be 180)
        :return: move command value (left/right) and num of steps that need to be done
        """
        num_of_degrees = abs(car.direction - next_direction)
        direction = None
        if num_of_degrees > 180:
            num_of_steps = (int)((360 - num_of_degrees)/RIGHT_LEFT_DEGREE)
            direction = MOVE_COMMANDS.Left
        else:
            num_of_steps = (int)((num_of_degrees)/RIGHT_LEFT_DEGREE)
            direction = MOVE_COMMANDS.Right

        return num_of_steps, direction


    def update_car_next_step(self ,car, prev_car_position):
        """
        Update the car's direction based on the current and previous positions.

        :param car: Car object
        :param prev_car_position: Tuple of previous car position in matrix
        """
        if car.position[0] == prev_car_position[0] and car.position[1] > prev_car_position[1]:
            car.next_step = DIRECTIONS.Right
        elif car.position[0] == prev_car_position[0] and car.position[1] < prev_car_position[1]:
            car.next_step = DIRECTIONS.Left
        elif car.position[0] > prev_car_position[0] and car.position[1] == prev_car_position[1]:
            car.next_step = DIRECTIONS.Down
        elif car.position[0] < prev_car_position[0] and car.position[1] == prev_car_position[1]:
            car.next_step = DIRECTIONS.Up
