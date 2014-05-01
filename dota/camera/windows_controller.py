import pythoncom, pyHook 
import sys
import json
import datetime as dt
from dota_camera import DotaCamera

running = False

def OnKeyboardEvent(event):
    global running
    # On K set running to true
    if event.Key == 'K':
        running = not running
    return True

def control_camera(camera_positions):
    """
    Control the Dota 2 replay camera based on a file of camera positions.
    Press K to start.
    """
    
    # Load the positions
    with open(camera_positions, 'r') as infile:
        camera_positions = json.load(infile)
        
    # Load camera control module
    camera = DotaCamera()
    
    # Go through each position
    for i, pos in enumerate(camera_positions):
        pythoncom.PumpWaitingMessages()
        if i == 500 or not running:
            break
        start_time = dt.datetime.now()
        # Set camera to the right position
        x = pos['x']
        y = pos['y']
        camera.set(x, y)
        camera.follow(0)
        #print x, y vfced
        print pos['time']
        
        # Wait a certain amount of time if we're not at the end
        if i != len(camera_positions) - 1:
            wait_time = camera_positions[i+1]['time'] - pos['time']
            while True:
                diff = dt.datetime.now() - start_time
                if (diff.microseconds / 1e6) >= wait_time:
                    break

def main():
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    
    # Wait until user presses a key
    while not running:
        pythoncom.PumpWaitingMessages()
    
    print "Starting program!"
    
    control_camera('camera_positions.json')
    
if __name__ == "__main__":
    main()