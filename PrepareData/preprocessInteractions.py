"""
Take all interactions and calculate pair wise jaccard index
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Interactions import Interaction
import itertools
import pickle
import json
import logging
import signal
import traceback
import resource



INTERACTION_DATA = "../data/TheGoodPlace_interactions.p"
USER_FILE = "../data/TheGoodPlace.csv"

def main():

    signal.signal(signal.SIGUSR1, lambda sig, stack: traceback.print_stack(stack))
    inter = Interaction(INTERACTION_DATA, type='p')
    users = read_users(USER_FILE)
    output = INTERACTION_DATA.rpartition('.')[0]
    logging.basicConfig(filename="preprocess1.log", level=logging.NOTSET, format='%(asctime)s %(message)s')

    pair_wise = dict()
    count = 0
    for user1, user2 in itertools.combinations(users, 2):
        stats = get_stats(user1, user2, inter)
        pair_wise[frozenset((user1, user2))] = stats
        count += 1
        if count % 10000 == 0:
            logging.info('{} pairs done'.format(count))
            logging.info(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            #print(pair_wise)
            #break
    pickle.dump(pair_wise, open(output + '_pairs.p', 'wb'))
    json.dump(pair_wise, open(output + '_pairs.json', 'w'))

def get_stats(user1, user2, interactions):
    stats = {}
    stats['retweet_jac'] = interactions.retweet_jaccard(user1, user2)
    #print(stats)
    return stats


def read_users(user_file):
    with open(user_file, 'rb') as f:
        users = map(int, f.readlines())
    return users


if __name__ == "__main__":
    main()