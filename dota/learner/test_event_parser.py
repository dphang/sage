from individual_event import IndividualEvent
from team_event import TeamEvent

class TestEventParser:
    """
    Builds 5-second events that need to be classified.
    """
    
    def __init__(self, data, interval=5):
        self.data = data
        self.interval = interval
    
    def build_test_events(self):
        time_data = self.data['time_data']
        start = time_data[0]['time']
        count = 0
        individual_events = []
        team_events = []
        for i in xrange(1, len(time_data)):
            previous_time = time_data[i-1]['time']
            current_time = time_data[i]['time']
            count += current_time - previous_time
            if count >= 5 or i == len(time_data) - 1:
                count = 0
                
                # Potentially each 5-second segment could correspond to any hero
                for i in xrange(10):
                    data = self.build_event_data(start, current_time)

                    individual_event = IndividualEvent(data, i, current_time-start)
                    individual_events.append(individual_event)
                    
                team_event = TeamEvent(data, current_time-start)
                #team_events.append(team_event)
                
                start = current_time
                
        return individual_events, team_events
    
    def build_event_data(self, start, end):
        """
        Builds only the data relevant to this event.
        We perform a binary search since the temporal data is already sorted by timestamp.
        """
        
        left = self.search_left(start)
        right = self.search_right(end)
    
        return self.data['time_data'][left:right + 1]
    
    def search_left(self, time, lo=None, hi=None):
        if lo == None:
            lo = 0
        if hi == None:
            hi = len(self.data['time_data']) - 1
            
        middle = (lo + hi) / 2
        if lo > hi:
            return middle
        
        test_time = self.data['time_data'][middle]['time']
        if time < test_time:
            return self.search_left(time, lo, middle - 1)
        elif time > test_time:
            return self.search_left(time, middle + 1, hi)
        else:
            return middle
        
    def search_right(self, time, lo=None, hi=None):
        if lo is None:
            lo = 0
        if hi is None:
            hi = len(self.data['time_data']) - 1
            
        middle = (lo + hi) / 2
        if lo > hi:
            temp = middle + 1
            if temp == len(self.data['time_data']):
                return -1
            else:
                return temp
        
        test_time = self.data['time_data'][middle]['time']
        if time < test_time:
            return self.search_right(time, lo, middle - 1)
        elif time > test_time:
            return self.search_right(time, middle + 1, hi)
        else:
            return middle        
                
        
