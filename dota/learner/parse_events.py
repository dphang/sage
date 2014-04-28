import json
from training_event_parser import TrainingEventParser
from test_event_parser import TestEventParser
from learner import Learner

def main():
    with open('replay_data.json', 'r') as infile:
        replay_data = json.load(infile)

    with open('replay_events.json', 'r') as infile:
        replay_events = json.load(infile)
        
    # Create event parser to parse our events from training data
    # Ideally, do this for more than one replay
    training_parser = TrainingEventParser(replay_data, replay_events)
    individual_events, team_events = training_parser.parse_events()
    
    # Write all events into training data set
    with open('training_data/individual_events.json', 'w') as outfile:
        json.dump(list(individual_events), outfile, indent=4)
        
    with open('training_data/team_events.json', 'w') as outfile:
        json.dump(list(team_events), outfile, indent=4)
        
    # Use our test event parser to create 5-second events from test data.
    test_parser = TestEventParser(replay_data)
    
    """
    test_individual_events, test_team_events = test_parser.build_test_events()
    
    with open('test_data/individual_events.json', 'w') as outfile:
        tmp = [event.feature_vector() for event in test_individual_events]
        json.dump(tmp, outfile, indent=4)
    """
    
    # Classify team events first
    
    
    # Classify individual events second
    
        
    # Create a classifier
    #individual_learner = Learner(individual_events, tmp)
    #individual_learner.train(individual_events[0], individual_events[1])
    #print individual_learner.classify([2.5, 3.0])
    #team_learner = Learner()

if __name__ == '__main__':
    main()