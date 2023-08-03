from ESP32CAM_Car.Movement import move
from .Detection_Handler.Detection_controller import Detection_controller
from Data_Structures import *
import BFS_Logic
from ESP32CAM_Car.MovementAPI import move

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


angle_to_direction = {
    'Left': 0,
    'Right': 180,
    'Up': 90,
    'Down': 270
}


class Movement_Handler():

    def __init__(self):
        self.Detection_controller = Detection_controller()
        self.BFS_Logic = BFS()
        self.car = Car()
        self.car_arrived_to_maneuver_point = False
        self.car_arrived_to_destination = False
        self.parking_slot_dest = None
        self.parking_slots = Parking_Slots()
        self.in_process = False

    def get_car_position(self):
        return self.car.get_position()

    def get_car_position_in_matrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == Val_dict["CAR"]:
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
            nearest_parking_slot_path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(),
                                                                    self.car.get_position(), self.slot)
            if len(nearest_parking_slot_path) < dist_nearest_parking_slot:
                dist_nearest_parking_slot = len(nearest_parking_slot_path)
                chosen_slot = slot

        self.parking_slot_dest = chosen_slot

    def car_movement(self, matrix):
        path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(), self.car.get_position(),
                                           self.parking_slot_dest)
        if path is None:
            print("No valid path found.")
            return

        for i in range(len(path) - 1):
            current_cell = path[i]
            next_cell = path[i + 1]

            next_direction = self.get_next_direction(current_cell, next_cell)
            update_car_angle(self.car, angle_to_direction.get(next_direction))

            # Move the car forward (you need to implement this part)
            # TODO: Understand how much forward need to move!?!?
            self.move_car_forward()

    @staticmethod
    def update_car_angle(car, next_direction):
        """
        :param car: object car for getting current angle of car
        :param next_direction: next direction in degrees (if right needed, it would be 180)
        :return: move command value (left/right) and num of steps that need to be done
        """
        car_tilt_degrees = car.get_direction_degrees()  # 315 --> 0
        num_of_degrees = abs(car_tilt_degrees - next_direction)  # =315
        direction = None
        if num_of_degrees > 180:
            num_of_steps = (int)((360 - num_of_degrees) / RIGHT_LEFT_DEGREE)
            direction = MOVE_COMMANDS.RIGHT
        else:
            num_of_steps = (int)((num_of_degrees) / RIGHT_LEFT_DEGREE)
            direction = MOVE_COMMANDS.LEFT

        move_to_correct_angle(num_of_steps, direction)

    @staticmethod
    def move_to_correct_angle(num_of_moves: int, direction: MOVE_COMMANDS):
        for i in range(num_of_moves):
            move(angle_to_direction)

    @staticmethod
    def get_next_direction(curr_position: Cell, dest_position: Cell):
        """
        Update the car's direction based on the current and destination positions.
        Assuming there 4 options to move!!
        :param curr_position: Current position cell
        :param dest_position: Destination position cell
        """
        if curr_position.x == dest_position.x and curr_position.y < dest_position.y:
            dir_to_move = DIRECTIONS.Right
        elif curr_position.x == dest_position.x and curr_position.y > dest_position.y:
            dir_to_move = DIRECTIONS.Left
        elif curr_position.x < dest_position.x and curr_position.y == dest_position.y:
            dir_to_move = DIRECTIONS.Down
        elif curr_position.x > dest_position.x and curr_position.y == dest_position.y:
            dir_to_move = DIRECTIONS.Up

        return dir_to_move
