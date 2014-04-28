from individual_event import IndividualEvent
from team_event import TeamEvent

class TrainingEventParser:
    """
    Parses both individual and team events from training replay data into a suitable format for machine learning.
    """
    
    def __init__(self, data, events):
        self.data = data
        self.events = events
    
    def parse_events(self):
        # Separate into individual or team events
        # Tuples are (feature_vectors, labels)
        individual_events = ([], [])
        team_events = ([], [])
        
        for event in self.events:
            start = event['start']
            end = event['end']
            label = event['label']
            hero = event['hero']
            
            # Build five second intervals for each event
            for i in xrange(start, end-4):
                if hero is not None:
                    # An individual event
                    data = self.build_event_data(i, i+5)
                    individual_event = IndividualEvent(data, hero, 5, label)
                    
                    # Append feature vector and label
                    individual_events[0].append(individual_event.feature_vector())
                    individual_events[1].append(individual_event.label)
                else:
                    # Team events
                    data = self.build_event_data(i, i+5)
                    team_event = TeamEvent(data, 5, label)
                    
                    # Append feature vector and label
                    team_events[0].append(team_event.feature_vector())
                    team_events[1].append(team_event.label)
        
        # Return both types of events
        return individual_events, team_events
        
    def build_event_data(self, start, end):
        """
        Builds only the data relevant to this event.
        We perform a binary search since the temporal data is already sorted by timestamp.
        """
        
        left = self.search_left(start)
        right = self.search_right(end)
    
        return self.data['time_data'][left:right+1]
    
    def search_left(self, time, lo=None, hi=None):
        if lo == None:
            lo = 0
        if hi == None:
            hi = len(self.data['time_data'])-1
            
        middle = (lo+hi)/2
        if lo > hi:
            return middle
        
        test_time = self.data['time_data'][middle]['time']
        if time < test_time:
            return self.search_left(time, lo, middle-1)
        elif time > test_time:
            return self.search_left(time, middle+1, hi)
        else:
            return middle
        
    def search_right(self, time, lo=None, hi=None):
        if lo is None:
            lo = 0
        if hi is None:
            hi = len(self.data['time_data'])-1
            
        middle = (lo+hi)/2
        if lo > hi:
            temp = middle+1
            if temp == len(self.data['time_data']):
                return -1
            else:
                return temp
        
        test_time = self.data['time_data'][middle]['time']
        if time < test_time:
            return self.search_right(time, lo, middle-1)
        elif time > test_time:
            return self.search_right(time, middle+1, hi)
        else:
            return middle