"""
helper methods to get all indices
input : interactions file json or pickel

"""
import pickle
import json


class Interaction:

    def __init__(self, file_name, type='p'):
        '''
        :param file_name: file containing interactions
        :param type: "json" or "p"
        '''
        self.interactions = Interaction.load_file(file_name, type)
        self.memoise = dict()

    def retweet_jaccard(self, user1, user2):
        key = (user1, user2)
        if(key  in self.memoise):
            return self.memoise[key]
        user1_retweet_set = list(self.interactions[int(user1)]['retweets'].keys())
        user2_retweet_set = list(self.interactions[int(user2)]['retweets'].keys())
        jac = Interaction.jaccard(user1_retweet_set, user2_retweet_set)
        self.memoise[key] = jac
        return jac

    @staticmethod
    def load_file(filename, type):
        if type == 'p':
            interactions = pickle.load(open(filename, 'rb'))
        else:
            interactions = json.load(open(filename, 'r'))
        return interactions

    @staticmethod
    def jaccard(a, b):
        union = list(set(a + b))
        set_a = set(a)
        set_b = set(b)
        intersection = list(set_a - (set_a - set_b))
        # print(intersection)
        if len(union) == 0:
            return 0
        jaccard_coeff = float(len(intersection)) / len(union)
        return jaccard_coeff

