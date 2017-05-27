import json
from Variables.Variable import Variable
from Utils.Utils import *

class X4Sentiment(Variable):
    def __init__(self, g, json_file):
        super().__init__("Sentiment")
        self.network = g
        self.sentiment = self.parse_sentiment(
                json.load(open(json_file)),
                self.network.start_date,
                self.network.stop_step,
                self.network.intervals)

    def get_covariate(self, node, current_date, nonadopted):
        """
        Overwrite get_covariate function
        :param node: 
        :param current_date: 
        :param nonadopted: 
        :return:                sentiment varialbe of node at current_date 
        """
        step = date_to_step(current_date, self.network.start_date, self.network.intervals)
        return self.sentiment[node][step]

    def parse_sentiment(self, json_data, start_date, stop_step, intervals, debug=False):
        """
        Combine the raw sentiment data measure in second into data measure by step length.
        :return: Dictionary format data
        {
            "User1": [
                average_sentiment_value1,       # Step 0 
                average_sentiment_value2,       # Step 1
                average_sentiment_value3,       # Step 2
                average_sentiment_value4,       # Step 3
            ],
            "User2": [
                average_sentiment_value1, 
                average_sentiment_value2, 
                average_sentiment_value3, 
                average_sentiment_value4, 
            ]

        }
        """
        sentiment_data = self.parse_sentiment_data_by_step(json_data, start_date, stop_step, intervals)
        average_data = {}
        for user_id, data_by_weeks in sentiment_data.items():
            average_data[user_id] = []
            for week in data_by_weeks:
                if week == [] and len(average_data[user_id]) == 0:
                    average_data[user_id].append(0)
                elif week == []:
                    average_data[user_id].append(average_data[user_id][-1])
                else:
                    average_data[user_id].append(sum(week) / len(week))
        return average_data

    def parse_sentiment_data_by_step(self, json_data, start_date, stop_step, intervals, debug=False):
        """
        Combine the raw sentiment data measure in second into data measure by step length.
        :return: Dictionary format data
        {
            "User1": [
                [sentiment_value1, sentiment_value2, sentiment_value3], # Step 0
                [sentiment_value1, sentiment_value2, sentiment_value3], # Step 1
                [sentiment_value1, sentiment_value2], # Step 2
                [sentiment_value1, sentiment_value2]  # Step 3
            ],
            "User2": [
                [sentiment_value1, sentiment_value2], # Step 0
                [sentiment_value1, sentiment_value2], # Step 1
                [sentiment_value1], # Step 2
                [sentiment_value1]  # Step 3
            ]
        }
        """

        # def date_to_step(timestamp):
        #     if timestamp < start_date:
        #         return 0
        #     return (timestamp - start_date) // intervals

        if debug:
            print("start date: {}".format(start_date))

        sentiment_data = {}
        for user_id, messages in json_data.items():
            sentiment_data[user_id] = [[] for _ in range(stop_step + 1)]
            for date, sentiment_value in messages.items():
                step = min(stop_step, date_to_step(int(date), start_date, intervals))
                sentiment_data[user_id][step].append(sentiment_value)

                if debug:
                    print("{}({}): {}".format(date, step, sentiment_value))

        if debug:
            for k, v in sentiment_data.items():
                print("{} {}".format(k, v))

        return sentiment_data