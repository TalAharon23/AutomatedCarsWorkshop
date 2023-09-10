import time
import cv2
import threading

from ESP32CAM_Car.MovementAPI import move
from Detection_Handler.Detection_controller import Detection_controller
from Data_Structures import *
import BFS_Logic

RIGHT_LEFT_DEGREE = 3
delta_tilt_degrees = 5


class MOVE_COMMANDS:
    Forward = "go"
    Left = "left"
    Right = "right"
    Back = "back"
    Parking = "parking"


angle_to_direction_from_Move_Command = {
    MOVE_COMMANDS.Left: 270,
    MOVE_COMMANDS.Right: 90,
    MOVE_COMMANDS.Forward: 0,
    MOVE_COMMANDS.Back: 180
}


class DIRECTIONS:
    Up = "Up"
    Left = "Left"
    Right = "Right"
    Down = "Down"


angle_to_direction = {
    'Left': 270,
    'Right': 90,
    'Up': 0,
    'Down': 180
}

direction_to_angle = {
    270: 'Left',
    90: 'Right',
    0: 'Up',
    180: 'Down'
}


class Movement_Handler:

    def __init__(self):
        self.BFS_Logic = BFS_Logic.BFS()
        self.robot = Car()
        self.car_arrived_to_maneuver_point = False
        self.car_arrived_to_destination = False
        self.parking_slot_dest = None
        self.parking_slot_dest_angle = None
        self.parking_slots = Parking_Slots()
        self.in_process = True
        self.last_position = None
        self.last_direction = None
        self.last_turn = None
        self.counter = 0
        self.path_index = 0


    def reset_matrix_and_data(self):
        Detection_controller.reset_Matrix()
        test = self.parking_slots.get_parking_slots_description()[0]
        Detection_controller.insert_parking_slot_to_matrix(self.parking_slots.get_parking_slots_description()[0])

    # @staticmethod
    def start_car_parking_session(self):
        """
        Main loop for parking session.
        While
        :return:
        """
        dc = Detection_controller()
        time.sleep(1.5)
        while Detection_controller.isVideoOnLive() and self.in_process:

            if self.counter % 7 == 0:
                # set parking destination
                if len(self.parking_slots.get_parking_slots()) == 0:
                    self.counter += 1
                    continue

                if self.parking_slot_dest is None:
                    if len(self.parking_slots.get_parking_slots()) == 0 or self.robot.position is None:
                        self.move_car_diagonally()
                        continue

                    self.set_parking_slot_destination()

                time.sleep(0.2)
                if self.check_validation():
                    if self.counter % 3 == 0:
                        move(MOVE_COMMANDS.Forward)
                    self.car_movement()
                else:
                    try:
                        self.handle_validation_error()
                    except:
                        self.move_car_diagonally()

            self.counter += 1

    def check_if_arrived(self):
        if self.parking_slot_dest is not None and self.robot.get_position() is not None and self.robot.get_position().X():
            if abs(self.robot.get_position().X() - self.parking_slot_dest.X()) < 12 and abs(
                    self.robot.get_position().Y() - self.parking_slot_dest.Y()) < 14:
                while (self.robot.get_direction_degrees() < self.parking_slot_dest_angle - 5 or
                       self.robot.get_direction_degrees() > self.parking_slot_dest_angle + 5):
                    self.update_car_angle(self.parking_slot_dest_angle)

                move(MOVE_COMMANDS.Parking)
                self.update_car_angle(self.parking_slot_dest_angle)
                self.centerlize_car_inside_parking_slot()
                print("Parking successful!")
                print("Parking successful!")
                print("Parking successful!")
                print("Parking successful!")
                self.in_process = False

    def centerlize_car_inside_parking_slot(self):
        parking_slot_y_origin = self.parking_slot_dest.Y() - y_parking_delta

        while abs(self.robot.get_position().Y() - parking_slot_y_origin) > 5:
            if self.robot.get_position().Y() > parking_slot_y_origin:
                move(MOVE_COMMANDS.Back)
            else:
                move(MOVE_COMMANDS.Forward)

    def check_validation(self):
        time.sleep(0.2)
        curr_position = self.robot.position
        curr_direction = self.robot.direction_degrees

        if curr_position is None:
            # The robot was not found
            print("check_validation - False\n")
            return False

        if self.last_position is not None:
            if self.last_position == curr_position and self.last_direction == curr_direction:
                print("check_validation - False\n")
                return False

        self.last_position = self.robot.position
        self.last_direction = self.robot.direction_degrees
        print("check_validation - True\n")
        return True

    def handle_validation_error(self):
        num_attempts = 0
        max_attempts = 10
        detection_successful = False

        while num_attempts < max_attempts and not detection_successful:
            # Move the car little to the right and forward
            if self.path is not None:
                for i in range(self.path_index, 5):
                    print("handle_validation_error - moving on path\n")
                    current_cell = self.path[i]
                    next_cell = self.path[i + 1]

                    next_direction = Movement_Handler.get_next_direction(current_cell, next_cell)
                    self.update_car_angle(angle_to_direction.get(next_direction))
            else:
                self.move_car_diagonally()

            # Check if the car is now detected
            if self.check_validation():
                detection_successful = True
            else:
                num_attempts += 1
                self.move_car_diagonally()

        if not detection_successful:
            # Raise an exception or set a flag indicating the car couldn't be detected
            raise Execption("Car couldn't be detected after multiple attempts")

    def move_car_diagonally(self):
        if self.last_turn is None or self.last_turn == MOVE_COMMANDS.Forward or self.last_turn == MOVE_COMMANDS.Back:
            self.last_turn = MOVE_COMMANDS.Left

        move(MOVE_COMMANDS.Forward)
        move(MOVE_COMMANDS.Forward)
        move(MOVE_COMMANDS.Forward)
        move(self.last_turn)
        move(self.last_turn)
        if self.check_validation():
            return
        move(self.last_turn)
        move(self.last_turn)
        move(self.last_turn)
        if self.check_validation():
            return
        move(self.last_turn)
        move(self.last_turn)
        move(self.last_turn)
        if self.check_validation():
            return
        move(self.last_turn)
        move(self.last_turn)
        move(self.last_turn)
        if self.check_validation():
            return
        move(self.last_turn)
        move(self.last_turn)
        if self.check_validation():
            return
        move(self.last_turn)
        move(self.last_turn)
        move(MOVE_COMMANDS.Back)

    def set_parking_slot_destination(self):
        chosen_parking_slot_index = 0
        parking_slots = self.parking_slots.get_parking_slots()
        chosen_slot = parking_slots[chosen_parking_slot_index]
        dist_nearest_parking_slot = len(self.BFS_Logic.shortestPath(Detection_controller.get_matrix(),
                                                                    self.robot.get_position(), chosen_slot))
        if parking_slots:
            for slot in parking_slots:
                nearest_parking_slot_path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(),
                                                                        self.robot.get_position(), slot)
                self.parking_slot_dest_angle = self.parking_slots.get_parking_angles()[chosen_parking_slot_index]
                if len(nearest_parking_slot_path) < dist_nearest_parking_slot:
                    dist_nearest_parking_slot = len(nearest_parking_slot_path)
                    chosen_slot = slot
                    self.parking_slot_dest_angle = self.parking_slots.get_parking_angles()[chosen_parking_slot_index]

                chosen_parking_slot_index += 1

        self.parking_slot_dest = chosen_slot

    def car_movement(self):
        self.path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(), self.robot.get_position(),
                                                self.parking_slot_dest)
        if self.path is None:
            print("No valid path found")
            return

        index = self.next_cell_optimization()
        current_cell = self.path[index]
        if index + 1 < len(self.path):
            next_cell = self.path[index + 1]
            self.print_BFS_in_matrix()
            self.check_if_arrived()
            if self.in_process:
                next_direction = Movement_Handler.get_next_direction(current_cell, next_cell)
                self.update_car_angle(angle_to_direction.get(next_direction))
                self.check_if_arrived()
                self.reset_robot_data()
                self.path_index = self.path_index + 1
            else:
                self.reset_matrix_and_data()

    def print_BFS_in_matrix(self):
        origin_matrix = Detection_controller.get_matrix()
        for cell in self.path:
            origin_matrix[cell.Y(), cell.X()] = Val_dict.BFS_ROAD

        Detection_controller.set_matrix(origin_matrix)

    def update_car_angle(self, next_direction):
        """
        :param car: object car for getting current angle of car
        :param next_direction: next direction in degrees (if right needed, it would be 180)
        :return: move command value (left/right) and num of steps that need to be done
        """
        car_tilt_degrees = self.robot.get_direction_degrees()
        abs_num_of_degrees = min(abs(car_tilt_degrees - next_direction), 360 - abs(car_tilt_degrees - next_direction))
        num_of_degrees = car_tilt_degrees - next_direction
        direction = None

        while abs_num_of_degrees > delta_tilt_degrees and self.in_process:
            if num_of_degrees > 180:
                num_of_degrees = 360 - (car_tilt_degrees - next_direction)
                num_of_steps = int(num_of_degrees / RIGHT_LEFT_DEGREE)
                direction = MOVE_COMMANDS.Right
            elif 0 < num_of_degrees < 180:
                num_of_degrees = car_tilt_degrees - next_direction
                num_of_steps = int(num_of_degrees / RIGHT_LEFT_DEGREE)
                direction = MOVE_COMMANDS.Left
            elif 0 > num_of_degrees > -180:
                num_of_degrees = abs(car_tilt_degrees - next_direction)
                num_of_steps = int(num_of_degrees / RIGHT_LEFT_DEGREE)
                direction = MOVE_COMMANDS.Right
            else:
                num_of_degrees = 360 - abs(car_tilt_degrees - next_direction)
                num_of_steps = int(num_of_degrees / RIGHT_LEFT_DEGREE)
                direction = MOVE_COMMANDS.Left

            if direction != MOVE_COMMANDS.Forward:
                move(direction)

            if not self.in_process:
                self.reset_matrix_and_data()

            car_tilt_degrees = self.robot.get_direction_degrees()
            abs_num_of_degrees = min(abs(car_tilt_degrees - next_direction),
                                     360 - abs(car_tilt_degrees - next_direction))
            num_of_degrees = car_tilt_degrees - next_direction

        if abs_num_of_degrees <= delta_tilt_degrees:
            num_of_steps = 1
            move(MOVE_COMMANDS.Forward)

        print(f"num_of_steps: {num_of_steps}\n")

        self.last_turn = direction

    @staticmethod
    def get_next_direction(curr_position: Cell, dest_position: Cell):
        """
        Update the car's direction based on the current and destination positions.
        Assuming there 4 options to move!!
        :param curr_position: Current position cell
        :param dest_position: Destination position cell
        """
        if curr_position.x == dest_position.x and curr_position.y < dest_position.y:
            dir_to_move = DIRECTIONS.Down
        elif curr_position.x == dest_position.x and curr_position.y > dest_position.y:
            dir_to_move = DIRECTIONS.Up
        elif curr_position.x < dest_position.x and curr_position.y == dest_position.y:
            dir_to_move = DIRECTIONS.Right
        elif curr_position.x > dest_position.x and curr_position.y == dest_position.y:
            dir_to_move = DIRECTIONS.Left

        return dir_to_move

    def reset_robot_data(self):
        self.robot.position = None
        self.robot.direction_degrees = None

    def set_process_val(self, is_in_process: bool):
        self.in_process = is_in_process

    def next_cell_optimization(self):
        first_direction_change = 0
        if len(self.path) > 24:

            for index in range(0, min(len(self.path), 21)):
                current_cell = self.path[index + 2]
                previous_cell = self.path[index + 1]

                # Determine directions for current and previous cells
                current_direction = Movement_Handler.get_next_direction(previous_cell, current_cell)
                previous_direction = Movement_Handler.get_next_direction(self.path[index], previous_cell)

                # Check for direction change
                if current_direction != previous_direction:
                    first_direction_change = index + 2
                    break

            if first_direction_change is not None:
                self.robot.set_position(self.path[first_direction_change])

        return first_direction_change

    def get_tilt_delta(self, next_direction):
        car_tilt_degrees = self.robot.get_direction_degrees()
        abs_num_of_degrees = min(abs(car_tilt_degrees - next_direction), 360 - abs(car_tilt_degrees - next_direction))

        return abs_num_of_degrees
