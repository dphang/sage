"""
Programmatically controls the Dota 2 camera given a JSON-encoded list of timestamps and coordinates.
Note that since Dota 2 has no official API for controlling the replay camera, we use a hacky approach:
controlling the camera using a series of mouse events.

Input: JSON-encoded list of timestamps and coordinates
"""

import sys, select
import json
import datetime as dt
from dota_camera import DotaCamera

def control_camera(filename):
    """
    Control the Dota 2 replay camera based on a file of camera positions.
    Press K to start.
    """
    
    # Load the positions
    with open(filename, 'r') as infile:
        camera_positions = json.load(infile)
        
    # Load camera control module
    camera = DotaCamera()
    
    # Go through each position
    for i, pos in enumerate(camera_positions):
        # Break if enter is pressed
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = raw_input()
            break
        start_time = dt.datetime.now()
        # Set camera to the right position
        x = pos['x']
        y = pos['y']
        #camera.set(x, y)
        
        # Wait until the next time the camera needs to be moved
        if i != len(camera_positions) - 1:
            wait_time = camera_positions[i+1]['time'] - pos['time']
            while True:
                diff = dt.datetime.now() - start_time
                if (diff.microseconds / 1e6) >= wait_time:
                    break
                
if __name__ == "__main__":
    control_camera('camera_positions.json')
        
    
    
    