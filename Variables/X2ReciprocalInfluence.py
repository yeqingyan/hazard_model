"""
Social influence from
reciprocal relationships:
common bond theory;cohesion

X2i(t-1)

number of all adopted reciprocal neighbors at time t-1 for node i, weighted by the strength of interaction frequency on a normalized 0-1 scale (distinguishing strong from weak ties)
normalization is done by dividing the each neighbors interaction withy total neighbors (adopted + non-adopted) interactions
"""

from Variables.Variable import Variable
from Utils.Interactions import Interaction
import math
import pickle
from Utils.Utils import *
import json

class X2reciprocalInfluence(Variable):
    def __init__(self, g, interactions_file, file_type='p'):
        super().__init__("reciprocal_influence")
        self.network = g
        #self.interaction = self.load_file(interactions_file)
        self.interaction = Interaction(interactions_file)

    def get_covariate(self, node, current_date, nonadopted):
        """
        Overwrite get_covariate function
        :param node:
        :param current_date:
        :param nonadopted:
        :return: retweet Jaccard varialbe of node at current_date
        """
        friends = self.network.friends(node, current_date)
        total_reciprocal = 0
        current_influence = []
        total_friends = len(friends)
        reci_friends = 0
        reci_adopted = 0
        for each_friend in friends:
            friends_of_friend = self.network.friends(each_friend, current_date)

            # find reciprocal friend
            if node in friends_of_friend:
                reci_friends += 1
                inter_count = self.interaction.interaction_count(node, each_friend)
                total_reciprocal += inter_count
                if self.network.user_adopted_time(each_friend) <= current_date:
                    reci_adopted += 1
                    current_influence.append(inter_count)
        total_influence = 0
        for influence in current_influence:
            total_influence += float(influence) / float(total_reciprocal)
        #print("{} friends {} reciprocal {} adopted {} influence".format(total_friends, reci_friends, reci_adopted, total_influence))
        return total_influence




    def load_file(filename, file_type='p'):
        if file_type == 'p':
            interactions = pickle.load(open(filename, 'rb'))
        else:
            interactions = json.load(open(filename, 'r'))
        return interactions
