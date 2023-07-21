from ESP32CAM_Car.Movement import move
from .Detection_Handler.Detection_controller import Detection_controller
import Data_Structures
import BFS_Logic

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

    def get_car_position(self):
        return self.car.get_position()

    def get_car_position_in_matrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == VAL_DICT["Robot"]:
                    return i, j
        raise ValueError("Matrix does not contain the car.")

    def make_one_step(self):
        while

    def set_parking_slot_destination(self):
        chosen_slot = self.parking_slots[0]
        nearest_parking_slot_path = None
        dist_nearest_parking_slot = len(nearest_parking_slot_path)
        for slot in self.parking_slots:
            nearest_parking_slot_path = self.BFS_Logic.shortestPath(get_matrix, self.car.get_position(), self.slot)
            if len(nearest_parking_slot_path) < dist_nearest_parking_slot:
                dist_nearest_parking_slot = len(nearest_parking_slot_path)
                chosen_slot = slot

        self.parking_slot_dest = chosen_slot

    # def car_movement(matrix):
    #     car = Car()
    #     new_matrix = duplicate_matrix(matrix)
    #
    #     while matrix[car.position[0]][car.position[1]] == VAL_DICT["Path"]:
    #         move(MOVE_COMMANDS.Forward)
    #
    #         # Check if the car went out of line or hit an empty cell
    #         if not car.in_bounds(new_matrix) or new_matrix[car.position[0]][car.position[1]] == VAL_DICT["Empty"]:
    #             path_positions = find_positions(new_matrix, VAL_DICT["Path"])
    #             path_positions.remove(car.position)
    #
    #             # Try to turn right
    #             right_pos = car.right()
    #             if right_pos in path_positions:
    #                 move(MOVE_COMMANDS.Right)
    #             else:
    #                 # Try to turn left
    #                 left_pos = car.left()
    #                 if left_pos in path_positions:
    #                     move(MOVE_COMMANDS.Left)
    #
    #         # Update the car position in the new matrix
    #         new_matrix[car.position[0]][car.position[1]] = VAL_DICT["Robot"]
    #
    #     return new_matrix


    def update_car_direction(car, prev_car_position):
        """
        Update the car's direction based on the current and previous positions.

        :param car: Car object
        :param prev_car_position: Tuple of previous car position in matrix
        """
        if car.position[0] == prev_car_position[0] and car.position[1] > prev_car_position[1]:
            car.direction = DIRECTIONS.Right
        elif car.position[0] == prev_car_position[0] and car.position[1] < prev_car_position[1]:
            car.direction = DIRECTIONS.Left
        elif car.position[0] > prev_car_position[0] and car.position[1] == prev_car_position[1]:
            car.direction = DIRECTIONS.Down
        elif car.position[0] < prev_car_position[0] and car.position[1] == prev_car_position[1]:
            car.direction = DIRECTIONS.Up
