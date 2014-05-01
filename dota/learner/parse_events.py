import json
from training_event_parser import TrainingEventParser
from test_event_parser import TestEventParser
from learner import Learner
import random as r

def main():
    with open('../data/replay_data.json', 'r') as infile:
        replay_data = json.load(infile)

    with open('../data/replay_events.json', 'r') as infile:
        replay_events = json.load(infile)
        
    # Create event parser to parse our events from training data
    # Ideally, do this for more than one replay
    training_parser = TrainingEventParser(replay_data, replay_events)
    events, _ = training_parser.parse_events()
    
    # Write all events into training data set
    with open('training_data/events.json', 'w') as outfile:
        json.dump(list(events), outfile, indent=4)
        
    r.shuffle(events[0])
    # Write all events into test data set
    with open('test_data/events.json', 'w') as outfile:
        json.dump(events[0], outfile, indent=4)

if __name__ == '__main__':
    main()