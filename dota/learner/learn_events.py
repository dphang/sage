import json
from training_event_parser import TrainingEventParser
from test_event_parser import TestEventParser
from learner import Learner

def main():
    # Load individual events
    with open('training_data/events.json', 'r') as infile:
        training_data = json.load(infile)
    with open('test_data/events.json', 'r') as infile:
        test_data = json.load(infile)
    
    # Classify events
    learner = Learner()
    learner.train(training_data[0], training_data[1])
    
    test_labels = [learner.classify(i) for i in list(test_data)]
    test_labels = [str(i) for i in test_labels]
    
    with open('test_data/labels.json', 'w') as outfile:
        json.dump(list(test_labels), outfile, indent=4)    

if __name__ == '__main__':
    main()