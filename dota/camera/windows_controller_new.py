import pythoncom, pyHook 
import sys
import json
import datetime as dt
import time
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
    with open('events_fixed2.json', 'r') as infile:
        follows = json.load(infile)
        
    # Load camera control module
    camera = DotaCamera()
    
    # Go through each position
    for i, event in enumerate(follows):
        pythoncom.PumpWaitingMessages()
        
        # Break on pressing K
        if not running:
            break
        
        start_time = dt.datetime.now()
        # Set camera to follow the hero for thek event's duration
        hero_index = event['hero_index']
        duration = event['end'] - event['start']
        camera.reset()
        camera.follow(hero_index)
        print "Following", hero_index
        
        while True:
            pythoncom.PumpWaitingMessages()
            if not running:
                return
            diff = dt.datetime.now() - start_time

            if diff.seconds >= duration:
                print 'breaking'
                break

        camera.reset()

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