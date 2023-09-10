import requests
import time

# ESP32_ADDR = '10.100.102.30'
# ESP32_ADDR = '192.168.245.240'
# ESP32_ADDR = '10.100.102.30'
# ESP32_ADDR = '192.168.245.240'
# ESP32_ADDR = '172.20.10.3'
ESP32_ADDR = '192.168.131.240'



def move(direction: str):
    move_url = f'http://{ESP32_ADDR}/{direction}'
    response = requests.get(move_url)
    if response.status_code == 200:
        if direction == 'parking':
            print("Start parking!")
        else:
            print(f'Car moved {direction} successfully.')
    else:
        print(f'Failed to move the car {direction}.')

