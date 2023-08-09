import requests
import time

# ESP32_ADDR = '192.168.184.240'
ESP32_ADDR = '172.20.10.3'


class MOVE_COMMANDS:
    Forward = "go"
    Left = "left"
    Right = "right"
    Back = "back"


# ESP32_ADDR = ''


# def set_esp32_address(): # TODO: NEED TO GET PORT FROM TXT FILE!?
#     global ESP32_ADDR
#     # try:
#     with open('port.txt', 'r') as file:
#         ESP32_ADDR = file.read().strip()  # read the port number from the file and remove any whitespace
#     ESP32_ADDR = f'{ESP32_ADDR}'
#     return esp32_addr_str
#     except e:
#         print("Invalid esp32 address!!")
#         return None


def move(direction: str):
    # direction_command = "go" if "forward" else direction
    move_url = f'http://{ESP32_ADDR}/{direction}'
    response = requests.get(move_url)
    if response.status_code == 200:
        if direction == 'parking':
            print("Start parking!")
        else:
            print(f'Car moved {direction} successfully.')
    else:
        print(f'Failed to move the car {direction}.')


# EXAMPLE:
# def movement():
#     # Move forward for 2 seconds
#     move("go")
#     time.sleep(0.1)
#
#     # Turn right
#     move("parking")
#     time.sleep(0.3)  # Adjust this time as needed
#
#     # Move forward for 2 seconds
#     move("right")
#     time.sleep(0.1)
#
#     # Turn left
#     move("go")
#     time.sleep(0.1)  # Adjust this time as needed
#
#     # Move forward for 2 seconds
#     move("right")
#     time.sleep(0.3)
#
#     # parking the car
#     move("parking")


# def main():
#     # set_esp32_address()
#     # move_forward()
#     # movement()
#
#
# if __name__ == '__main__':
#     main()
