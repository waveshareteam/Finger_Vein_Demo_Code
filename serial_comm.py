import os
import re

def extract_board_identifier(full_model):
    model_rules = [
        #Raspberry Pi
        (r'Raspberry Pi 5', 'Pi5'),
        (r'Raspberry Pi 4', 'Pi4'),
        (r'Raspberry Pi 3', 'Pi3'),
        (r'Raspberry Pi Zero', 'Pi0'),
        (r'Raspberry Pi CM', 'PiCM'),

        #RDK Series
        (r'RDK X5', 'X5'),
        (r'RDK X5', 'X3'),
        {r'RDK S100', 'S100'}
    ]
    for pattern, identifer in model_rules:
        if re.search(pattern, full_model, re.IGNORECASE):
            return identifer
    return None

def get_board_info():
    board_info = {
        'type':  None,
        'model': None,
        'revision': None
    }
    if os.path.exists('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            #print(cpuinfo)
            if 'Raspberry Pi' in cpuinfo:
                board_info['type'] = 'RaspberryPi'
                model_match = re.search(r'Model\s+:\s*(.*)', cpuinfo)
                if model_match:
                    full_mode = model_match.group(1).strip()
                    board_info['model'] = extract_board_identifier(full_mode)
                    #print(board_info['model'])
                rev_match = re.search(r'Revision\s+:\s*(.*)', cpuinfo)
                if rev_match:
                    board_info['revision'] = rev_match.group(1).strip()
                return board_info
    

def get_serial_port():
    board = get_board_info()
    #print(f"The board is: {board['type']} {board['model'] or ''}")
    serial_map = {
        # Raspberry Pi Series
        'RaspberryPi': {
            'Pi5': '/dev/ttyAMA0',      # Raspberry Pi 5
            'Pi4': '/dev/ttyS0',        # Rspberry Pi 4
            'Pi3': '/dev/ttyS0',        # Rspberry Pi 3
            'Pi0': '/dev/ttyAMA0',      # Rspberry Pi Zero/Zero 2
            'PiCM': '/dev/ttyS0'        # Rspberry Pi Compute Module
            },
        # Jetson (reserved)
        'Jetson': {
            'Nano': '/dev/ttyTHS1',       # Jetson Nano
            'debug': '/dev/ttyS0'            # Debug port
        },
        # RDK Series
        'RDK': {
            'X5': '/dev/ttyS1',     # RDK X5
            'X3': '/dev/ttyS3',     # RDK X3
            'ultra': '/dev/ttyS2',  #RDK Ultra
            'S100': '/dev/ttyS1'    #RDK S100
        },
        # Unknow board
        'Unknown': {
            'default': '/dev/ttyACM0'        # Common use USB adapter
        }
    }
    return serial_map[board['type']][board['model']]

#print(get_serial_port())