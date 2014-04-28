#!/usr/bin/python

"""
Parses a Dota 2 replay file into a reduced dataset, which only pertains to hero data.
"""

import tarrasque
import json    

def main():
    replay = tarrasque.StreamBinding.from_file('demos/orange_navi.dem')
    
    # Append players
    players = {'radiant': [], 'dire': []}
    for player in replay.players:
        if player.team != 'spectator':
            players[player.team].append(player.name)
            
    # Read hero names
    hero_names = {}
    with open('hero_names.json', 'r') as infile:
        data = json.load(infile)
        
        for hero in data:
            for player in replay.players:
                if player.hero.name == hero['localized_name']:
                    hero_names[hero['name']] = (hero['localized_name'], player)
                    
    # Iterate through each tick, building our JSON data
    time_data = []
    for tick in replay.iter_ticks(start='pregame', end='postgame'):
        # Parse player time
        time = replay.info.game_time
        
        player_events = {}
        for player in replay.players:
            player_events[player.name] = []
            
        # Parse combat log events
        for event in replay.game_events:
            if event.name == 'dota_combatlog':
                # Attacker is a hero
                if event.attacker_name in hero_names:
                    # Target is a hero
                    if event.target_name in hero_names:
                        # Check if we are helping ally hero or attacking enemy hero
                        if hero_names[event.target_name][1].team != hero_names[event.attacker_name][1].team:
                            temp = "Attacked Hero"
                        else:
                            if hero_names[event.target_name][1].name == hero_names[event.attacker_name][1].name:
                                temp = "Helped Self"
                            else:
                                temp = "Helped Hero"
                    # Otherwise, we're attacking a creep
                    else:
                        temp = "Attacked Creep"
                    player_events[hero_names[event.attacker_name][1].name].append(temp)
                    
        # Parse player info
        player_info = []
        for player in replay.players:
            hero = player.hero
            x, y = hero.position
            player_info.append({'player': player.index, 'x': x, 'y': y, 'health': hero.health, 
                                'max_health': hero.max_health, 'mana': hero.mana, 'max_mana': hero.max_mana,
                                'events': player_events[player.name]})
                
        
        # Append to time data
        time_data.append({'time': time, 'player_info': player_info})
    
    # Write a JSON serialization
    with open('test.json', 'w') as outfile:
        json.dump({'players': players, 'time_data': time_data}, outfile, indent=4)
        
if __name__ == "__main__":
    main()
    