def get_hero_index(replay_data, replay_events):
    import random as r
    return r.randint(0, 9)        
"""
Parses a JSON-encoded data file into a list of camera movements.
Given replay data and game events, this will create a good set of camera movements.

We follow a hero-centric approach (i.e the camera follows only heroes), with
teamfights using a team hull approach (i.e the camera follows the center of the team, or
the hero that's doing a lot of actions).

This doesn't actually use any machine learning (that is only for detecting events)
although a good camera will:
- have smooth movement
- follow heroes accurately
- focus on interesting events when possible

Input: JSON-encoded file containing replay data and game events.
Output: JSON-encoded list of timestamps and coordinates
"""

import json

def generate_positions(data_filename, events_filename):
    """
    Generate camera movements based on replay data and replay events.
    """
    with open(data_filename, 'r') as infile:
        replay_data = json.load(infile)

    with open(events_filename, 'r') as infile:
        replay_events = json.load(infile)
        
    # Each interval lasts five seconds
    positions = []
    interval = 5
    
    # Go through each tick, randomly focusing on a hero
    elapsed_time = 0
    
    # Try first hero for now
    hero_index = 0
    
    time_data = replay_data['time_data']
    
    for i in xrange(len(time_data)):
        # If elapsed time is five seconds, we want to possibly focus on a different hero
        if elapsed_time >= interval:
            # Recalculate hero index
            hero_index = get_hero_index(replay_data, replay_events)
            pass
        
        if i != 0:
            # Increment elapsed time
            elapsed_time += time_data[i]['time'] - time_data[i-1]['time']
        
        # Compute the position of the camera
        time = time_data[i]['time']
        player = time_data[i]['player_info'][hero_index]
        
        x, y = player['x'], player['y']
        positions.append({'time': time, 'x': x, 'y': y})
    
    # Dump camera positions
    with open('camera_positions.json', 'w') as outfile:
        json.dump(positions, outfile, indent=4)
        
if __name__ == '__main__':
    generate_positions('../data/replay_data.json', '../data/replay_events.json')
        






