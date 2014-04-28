import json
from training_event_parser import TrainingEventParser
from test_event_parser import TestEventParser
from learner import Learner

def main():
    # Load individual events
    with open('training_data/individual_events.json', 'r') as infile:
        training_data = json.load(infile)
    with open('test_data/individual_events.json', 'r') as infile:
        test_data = json.load(infile)
    
    # Classify individual events
    individual_learner = Learner()
    individual_learner.train(training_data[0], training_data[1])
    for i in test_data:
        print individual_learner.classify(i)

if __name__ == '__main__':
    main()