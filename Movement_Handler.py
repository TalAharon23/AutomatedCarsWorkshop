from ESP32CAM_Car.Movement import move
from .Detection_Handler.Detection_controller import Detection_controller as DC
import Data_Structures

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



def get_car_position_in_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == VAL_DICT["Robot"]:
                return i, j
    raise ValueError("Matrix does not contain the car.")


def car_movement(matrix):
    car = Car()
    new_matrix = duplicate_matrix(matrix)

    while matrix[car.position[0]][car.position[1]] == VAL_DICT["Path"]:
        move(MOVE_COMMANDS.Forward)

        # Check if the car went out of line or hit an empty cell
        if not car.in_bounds(new_matrix) or new_matrix[car.position[0]][car.position[1]] == VAL_DICT["Empty"]:
            path_positions = find_positions(new_matrix, VAL_DICT["Path"])
            path_positions.remove(car.position)

            # Try to turn right
            right_pos = car.right()
            if right_pos in path_positions:
                move(MOVE_COMMANDS.Right)
            else:
                # Try to turn left
                left_pos = car.left()
                if left_pos in path_positions:
                    move(MOVE_COMMANDS.Left)

        # Update the car position in the new matrix
        new_matrix[car.position[0]][car.position[1]] = VAL_DICT["Robot"]

    return new_matrix


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
