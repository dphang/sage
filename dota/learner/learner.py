"""
Uses scikit-learn to train a knn classifier on a set of labeled replay data, in JSON format. We can then use this classifier
to classify similar important events in future replays.

Events have a few labels:

farm: hero is simply hitting creeps to gain experience and gold. This will be the default event should there be no other event.
gank: hero is attempting to ambush another hero
harass: hero casts a spell or attacks an enemy
teamfight: there is a teamfight
push: either team is pushing into the enemy's base

Based on these labels, this program will attempt to discover new events.
"""

from sklearn import neighbors, preprocessing

class Learner:
    """
    Learner using k nearest neighbors algorithm.
    """
    
    def __init__(self):
        self.nbrs = neighbors.KNeighborsClassifier(n_neighbors=1)
        self.scaler = preprocessing.data.StandardScaler()
        self.training_data = None
    
    def train(self, features, labels):
        """
        Train this learner on training data using k nearest neighbors
        """
        features = self.scaler.fit_transform(features)
        self.nbrs.fit(features, labels)
        
    def classify(self, features):
        """
        Classifies these examples
        """
        
        features = self.scaler.transform(features)
        return self.nbrs.predict(features)
