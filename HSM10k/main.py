import sys
import socket
import json
from struct import *

def load_config(filename):
    try:
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print(f"Config file '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in config file '{filename}'.")
        sys.exit(1)

def connect_to_hsm(config):
    try:
        hsmsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hsmsocket.connect((config['TCP_IP'], config['TCP_PORT']))
        return hsmsocket
    except socket.error as err:
        print(f"Socket error: {err}")
        sys.exit(1)

def send_command(socket, command):
    try:
        size = pack('>h', len(command))
        message = size + command
        socket.send(message)
        data = socket.recv(BUFFER_SIZE)
        return data.decode('utf-8')
    except socket.error as err:
        print(f"Error sending/receiving data: {err}")
        sys.exit(1)

if __name__ == "__main__":
    config = load_config("config.json")
    hsmsocket = connect_to_hsm(config)

    while True:
        # Rest of the script remains the same
        # ...
        # ...

    hsmsocket.close()
