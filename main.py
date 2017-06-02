import argparse
import datetime
import logging
import time

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DynamicNetwork import DynamicNetwork
from HazardModel import HazardModel
from Variables.X0Intercept import *
from Variables.X4Sentiment import *
from Variables.X1RetweetJaccard import X1RetweetJaccard
from Variables.X2ReciprocalInfluence import X2reciprocalInfluence
from Utils.NetworkUtils import *
from Utils.Plot import *

WEEK_IN_SECOND = 7 * 24 * 60 * 60
STOP_STEP = 13
SENTIMENT_DATA = "data/thegoodplace_sentiment_seconds.json"
INTERACTION_DATA = "data/TheGoodPlace_interactions.p"

class DateAction(argparse.Action):
    """
    Convert input string into date in seconds
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(DateAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string):
        start_date = int(time.mktime(datetime.datetime.strptime(values, "%m/%d/%Y").timetuple()))
        setattr(namespace, self.dest, start_date)

def config():
    program_description = "Hazard model"
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('g', help='Input network graph')
    parser.add_argument('-d', action=DateAction, help='Start date(m/d/y)')
    return vars(parser.parse_args())

def main():
    arguments = config()
    g = get_graphml(arguments['g'])
    #g = sample(g, 2000 / len(g))

    g = DynamicNetwork(g, start_date=arguments['d'], intervals=WEEK_IN_SECOND, stop_step=STOP_STEP)

    # TODO For Swati, put your varialbe here.
    variables = [
        X0Intercept(),
        #X4Sentiment(g, SENTIMENT_DATA)
        #X1RetweetJaccard(g, INTERACTION_DATA)
        X2reciprocalInfluence(g, INTERACTION_DATA)

    ]
    for v in variables:
        assert hasattr(v, 'name'), "Each variable must have a name attribute"

    hazard_model = HazardModel(g, variables)
    logging.info("Begin MLE estimation")
    # Step 1. MLE estimation
    ref_result, params = hazard_model.hazard_mle_estimation()

    # Step 2. Hazard model simulation
    sim_result, prob_dist = hazard_model.hazard_simulation(params)
    logging.info(sim_result)
    plot({"Reference": ref_result, "MLE result": sim_result}, show=False)

if __name__ == "__main__":
    logging.basicConfig(filename="hazard_X2.log", level=logging.NOTSET, format='%(asctime)s %(message)s')
    main()

