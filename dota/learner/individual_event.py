import numpy
import itertools

class IndividualEvent:
    """
    A Dota 2 individual event. This stores all information about a Dota 2 event, and allows us to calculate various numerical features. This involves
    only a single hero.
    """
    
    def __init__(self, data, index, length, label=None):
        self.label = label
        self.data = data
        self.index = index
        self.length = length
        
        # Properties
        self._displacement = None
        self._movement = None
        
    # Features computed for each event
    
    @property
    def displacement(self):
        """
        Displacement of a hero at the given index.
        """
        
        if self._displacement is None:
            last = len(self.data) - 1
            
            x_1, y_1 = self.data[0]['player_info'][self.index]['x'], self.data[0]['player_info'][self.index]['y']
            x_2, y_2 = self.data[last]['player_info'][self.index]['x'], self.data[last]['player_info'][self.index]['y']
             
            # We don't need the real distance, so we can avoid doing a square root
            self._displacement =  float((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
            
        return self._displacement

    @property
    def movement(self):
        """
        Movement of a hero at the given index.
        """
        
        if self._movement is None:
            self._movement = 0.0
            
            for i in xrange(1, len(self.data)):
                # Add the differences in positions
                x_1, y_1 = self.data[i-1]['player_info'][self.index]['x'], self.data[i-1]['player_info'][self.index]['y']
                x_2, y_2 = self.data[i]['player_info'][self.index]['x'], self.data[i]['player_info'][self.index]['y']
                
                # We don't need the real distance, so we can avoid doing a square root
                self._movement +=  (x_2 - x_1) ** 2 + (y_2 - y_1) ** 2
            
        return self._movement
    
    def feature_vector(self, time_scale=5):
        """
        Returns the feature vector of this event as a numpy array.
        Scaled into a default 5 second block.
        """
        
        scale = float(time_scale) / self.length
        return [scale * self.movement, scale * self.displacement]