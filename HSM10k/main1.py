import sys
import socket
import json
import os
import logging
from struct import *
from datetime import datetime

# Configure logging
log_folder = datetime.now().strftime("%Y-%m-%d")
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "hsm.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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
        logging.error(f"Socket error: {err}")
        sys.exit(1)

def send_command(socket, command):
    try:
        size = pack('>h', len(command))
        message = size + command
        socket.send(message)
        data = socket.recv(BUFFER_SIZE)
        return data.decode('utf-8')
    except socket.error as err:
        logging.error(f"Error sending/receiving data: {err}")
        sys.exit(1)

if __name__ == "__main__":
    config = load_config("config.json")
    hsmsocket = connect_to_hsm(config)

    while True:
        # Rest of the script remains the same
        # ...
        # ...

        # Log the response to the text file
        response = send_command(hsmsocket, command)
        logging.info(f"Response from HSM for {choice}: {response}")

    hsmsocket.close()
