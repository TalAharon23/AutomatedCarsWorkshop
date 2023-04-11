from ESP32CAM_Car.Movement import move

VAL_DICT = {
    "Empty": 0,
    "Border": 1,
    "Path": 2,
    "Parking_slot": 3,
    "Robot": 4
}


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


class Car:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction


def get_car_position_in_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == VAL_DICT["Robot"]:
                return i, j
    raise ValueError("Matrix does not contain the car.")


def car_movement(matrix):
    car = Car(get_car_position_in_matrix(matrix), DIRECTIONS.Right)
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
