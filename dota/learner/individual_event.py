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
        self._creep_attacks = None
        self._hero_attacks = None
        self._skill_uses = None
        self._health = None
        
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
    
    @property
    def creep_attacks(self):
        
        if self._creep_attacks is None:
            self._creep_attacks = 0
            
            for i in xrange(len(self.data)):
                events = self.data[i]['player_info'][self.index]['events']
                for e in events:
                    if e == 'Attacked Creep':
                        self._creep_attacks += 1
        
        return self._creep_attacks
    
    @property
    def hero_attacks(self):
        
        if self._hero_attacks is None:
            self._hero_attacks = 0
            
            for i in xrange(len(self.data)):
                events = self.data[i]['player_info'][self.index]['events']
                for e in events:
                    if e == 'Attacked Hero':
                        self._hero_attacks += 1
        
        return self._hero_attacks
    
    @property
    def skill_uses(self):
        
        if self._skill_uses is None:
            self._skill_uses = 0
            
            for i in xrange(len(self.data)):
                events = self.data[i]['player_info'][self.index]['events']
                for e in events:
                    if e == 'Helped Hero' or e == 'Helped Self':
                        self._skill_uses += 1
        
        return self._skill_uses
    
    @property
    def health(self):
        
        if self._health is None:
            self._health = 0.0
            
            max_health = health = self.data[0]['player_info'][self.index]['max_health']
            for i in xrange(len(self.data)):
                health = self.data[i]['player_info'][self.index]['health']
                self._health += health
                
            self._health = (health / len(self.data)) / float(max_health) 
            
        return self._health
            
    def feature_vector(self, time_scale=5):
        """
        Returns the feature vector of this event as a numpy array.
        Scaled into a default 5 second block.
        """
        
        scale = float(time_scale) / self.length
        return [scale * self.movement, scale * self.displacement, self.health, scale * self.creep_attacks, scale * self.hero_attacks, scale * self.skill_uses]