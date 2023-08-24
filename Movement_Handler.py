import time

import cv2
import threading

import Data_Structures
from ESP32CAM_Car.MovementAPI import move
from Detection_Handler.Detection_controller import Detection_controller
from Data_Structures import *
import BFS_Logic
from ESP32CAM_Car.MovementAPI import move

RIGHT_LEFT_DEGREE = 6


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




class Movement_Handler():

    def __init__(self):
        self.BFS_Logic                      = BFS_Logic.BFS()
        self.robot                          = Car()
        self.car_arrived_to_maneuver_point  = False
        self.car_arrived_to_destination     = False
        self.parking_slot_dest              = None
        self.parking_slots                  = Parking_Slots()
        self.in_process                     = True
        self.last_position                  = None
        self.last_direction                 = None
        self.last_turn                      = None
        self.counter                        = 0
        self.path_index                     = 0

    # @staticmethod
    def start_car_parking_session(self):
        """
        Main loop for parking session.
        While
        :return:
        """
        dc = Detection_controller()
        threading.Thread(target=dc.scan_video, args=[self.robot, self.parking_slots]).start()
        time.sleep(2)
        while (Detection_controller.isVideoOnLive() and self.in_process):

            if self.counter % 7 == 0:
                # processed_frame = Detection_controller.get_matrix(frame, self.robot, self.parking_slots)[0]
                # self.Detection_controller.out_video.write(processed_frame)
                # if self.counter % 30 == 0:
                #     dc.reset_Matrix()
                # set parking destination
                if len(self.parking_slots.get_parking_slots()) == 0:
                    self.counter += 1
                    continue
                    # self.parking_slots = self.Detection_controller.parking_slots.get_parking_slots()
                    # print(len(self.parking_slots))

                if self.parking_slot_dest == None:
                    if len(self.parking_slots.get_parking_slots()) == 0 or self.robot.position == None:
                        self.move_car_diagonally()
                        continue
                    # self.robot.set_position((0,0))
                    self.set_parking_slot_destination()
                time.sleep(0.6)
                if self.check_validation():
                    self.car_movement()
                else:
                    try:
                        self.handle_validation_error()
                    except:
                        self.move_car_diagonally()
            # else:
            #     self.Detection_controller.out_video.write(processed_frame)

            self.counter += 1

        #     q = cv2.waitKey(1)
        #     if q == ord("q"):
        #         break
        #
        # self.Detection_controller.out_video.release()
        # # release the src_video capture object
        # self.Detection_controller.src_video.release()
        # # Closes all the windows currently opened.
        # cv2.destroyAllWindows()


    def check_if_arrived_to_destination(self):
        car_x_position = self.robot.position[0]
        car_y_position = self.robot.position[1]
        parking_slot_x_position = self.parking_slot_dest[0]
        parking_slot_y_position = self.parking_slot_dest[1]
        if car_x_position != None and car_y_position != None and parking_slot_x_position != None and parking_slot_y_position != None:
            if abs(car_x_position - parking_slot_x_position) < 5 and abs(car_y_position - parking_slot_y_position):
                return True
        return False

    def check_validation(self):
        time.sleep(0.2)
        curr_position = self.robot.position
        curr_direction = self.robot.direction_degrees

        if curr_position == None:
            # The robot was not found
            print("check_validation - False\n")
            return False

        if self.last_position != None:
            if self.last_position == curr_position and self.last_direction == curr_direction:
                print("check_validation - False\n")
                return False

        self.last_position = self.robot.position
        self.last_direction = self.robot.direction_degrees
        print("check_validation - True\n")
        return True

    def handle_validation_error(self):
        num_attempts = 0
        max_attempts = 5
        detection_successful = False

        while num_attempts < max_attempts and not detection_successful:
            # Move the car little to the right and forward
            if self.path != None:
                for i in range(self.path_index, len(self.path) - 1):
                    print("handle_validation_error - moving on path\n")
                    current_cell = self.path[i]
                    next_cell = self.path[i + 1]

                    next_direction = self.get_next_direction(current_cell, next_cell)
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
        # Move the car 10 degrees to the right
        #self.update_car_angle(self.robot, self.robot.get_direction_degrees() + 40)  # tilt car to right 40 degrees
        # Move the car forward (you need to implement this part)
        if self.last_turn == None or self.last_turn == MOVE_COMMANDS.Forward or self.last_turn == MOVE_COMMANDS.Back:
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
        # Move the car back (you need to implement this part)
        move(MOVE_COMMANDS.Back)

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
        parking_slots = self.parking_slots.get_parking_slots()
        chosen_slot = parking_slots[0]
        nearest_parking_slot_path = chosen_slot
        dist_nearest_parking_slot = len(self.BFS_Logic.shortestPath(Detection_controller.get_matrix(),
                                                                        self.robot.get_position(), chosen_slot))
        if parking_slots:
            for slot in parking_slots:
                nearest_parking_slot_path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(),
                                                                        self.robot.get_position(), slot)
                if len(nearest_parking_slot_path) < dist_nearest_parking_slot:
                    dist_nearest_parking_slot = len(nearest_parking_slot_path)
                    chosen_slot = slot

        self.parking_slot_dest = chosen_slot

    def car_movement(self):
        self.path = self.BFS_Logic.shortestPath(Detection_controller.get_matrix(), self.robot.get_position(),
                                           self.parking_slot_dest)
        if self.path is None:
            print("No valid path found.")
            return

        # for i in range(len(self.path) - 1):
        current_cell = self.path[0]
        next_cell = self.path[0 + 1]

        next_direction = self.get_next_direction(current_cell, next_cell)
        self.update_car_angle(angle_to_direction.get(next_direction))
        self.reset_robot_data()
        self.path_index = self.path_index + 1

        # Move the car forward (you need to implement this part)
        # TODO: Understand how much forward need to move!?!?
        # move(MOVE_COMMANDS.Forward)
        # move(MOVE_COMMANDS.Forward)


    def update_car_angle(self, next_direction):
        """
        :param car: object car for getting current angle of car
        :param next_direction: next direction in degrees (if right needed, it would be 180)
        :return: move command value (left/right) and num of steps that need to be done
        """
        car_tilt_degrees = self.robot.get_direction_degrees()  # 315 --> 0
        num_of_degrees = abs(car_tilt_degrees - next_direction)  # =315
        direction = None
        if num_of_degrees > 15:
            # direction = (MOVE_COMMANDS.Right)
            # num_of_steps = 3
            # if car_tilt_degrees - num_of_degrees > 0:
            if (abs(next_direction - car_tilt_degrees) < 180 and car_tilt_degrees < next_direction or
                    car_tilt_degrees - next_direction < 180 and car_tilt_degrees > next_direction):
                num_of_steps = (int)(num_of_degrees / RIGHT_LEFT_DEGREE)
                direction = (next_direction + 180) % 360
                direction = (MOVE_COMMANDS.Right)
            else:
                num_of_degrees = abs(360 - num_of_degrees)  # =315
                num_of_steps = (int)((num_of_degrees) / RIGHT_LEFT_DEGREE)
                direction = MOVE_COMMANDS.Left
        else:
            num_of_steps = 2
            direction = MOVE_COMMANDS.Forward


        print(f"num_of_steps: {num_of_steps}\n")

        self.move_to_correct_angle(num_of_steps, direction)
        self.last_turn = direction
        time.sleep(4)

    def move_to_correct_angle(self, num_of_moves: int, direction):
        for i in range(num_of_moves):
            move(direction)

    def get_next_direction(self, curr_position: Cell, dest_position: Cell):
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