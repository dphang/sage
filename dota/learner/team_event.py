import numpy
import itertools

class TeamEvent:
    """
    A Dota 2 team event.
    """
    
    def __init__(self, data, length, label=None):
        self.label = label
        self.data = data
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
            
            #x_1, y_1 = self.data[0]['player_info'][self.index]['x'], self.data[0]['player_info'][self.index]['y']
            #x_2, y_2 = self.data[last]['player_info'][self.index]['x'], self.data[last]['player_info'][self.index]['y']
             
            # We don't need the real distance, so we can avoid doing a square root
            self._displacement =  0#float((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
            
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
                #x_1, y_1 = self.data[i-1]['player_info'][self.index]['x'], self.data[i-1]['player_info'][self.index]['y']
                #x_2, y_2 = self.data[i]['player_info'][self.index]['x'], self.data[i]['player_info'][self.index]['y']
                
                # We don't need the real distance, so we can avoid doing a square root
                self._movement +=  0#(x_2 - x_1) ** 2 + (y_2 - y_1) ** 2
            
        return self._movement
    
    def feature_vector(self, time_scale=5):
        """
        Returns the feature vector of this event as a numpy array.
        """
        
        scale = float(time_scale) / self.length
        return [scale * self.movement, scale * self.displacement]