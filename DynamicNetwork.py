import random
import networkx as nx

class DynamicNetwork:
    # Node attribute 'create_time' and edge attribute 'create_time' are different attributes.
    # Node's 'create_time' is the node's adoption time.
    # Edge's 'create_time' is when that edge created.
    ADOPTION_TIME = 'create_time'
    EDGE_CREATE_TIME = 'create_time'

    def __init__(self, g, start_date=None, intervals = None, stop_step = None):
        assert isinstance(g, nx.DiGraph), "Network must be instance of DiGraph"
        self.network = g
        # if sentiment_data == {}:
        #     self.fake_sentiment = True
        #     self.sentiment_data = {}
        # else:
        """
            Real sentiment data format
            {   "user_id1":
                    {   "timestamp1":   sentimentValue1,
                        "timestamp2":   sentimentValue2
                    }
                "user_id2":
                    {   "timestamp1":   sentimentValue1,
                        "timestamp2":   sentimentValue2
                    }
            }   
        """
        assert isinstance(intervals, int)
        assert start_date != None
        assert stop_step != None
        self.fake_sentiment = False
        self.start_date = start_date
        self.intervals = intervals
        self.stop_step = stop_step

    def users(self):
        return self.network.nodes()

    def user_adopted_time(self, node):
        # A node's create time is its adopted time.
        return self.network.node[node][self.ADOPTION_TIME]

    def friends(self, node, current_date):
        """ Return Twitter user's friends before the current_date
        A --> B means B is successor in our case it means A retweets B thus B influences A
        This pattern applies to quote reply and mentions

        :param node:                Current node
        :param current_date:        Date
        :return:                    Friends list
        """

        friends = []
        for friend in self.network.successors_iter(node):
            # return friends which edge node->friends was created before the current date
            if (self.network[node][friend][self.EDGE_CREATE_TIME] <= current_date):
                friends.append(friend)
        return friends

    def adopted_friends(self, node, current_date):
        """ Return number of adopted friends before current_date """
        friends = self.friends(node, current_date)
        adopted_friends = []

        for friend in friends:
            if self.user_adopted_time(friend) <= current_date:
                adopted_friends.append(friend)
        return adopted_friends

    def num_adopted_friends(self, node, current_date):
        return len(self.adopted_friends(node, current_date))

    def num_friends(self, node, current_date):
        return len(self.num_friends(node, current_date))

    def adopted_friends_percentage(self, node, current_date):
        """ Return percentage of adopted friends before current_date """
        num_friends = self.num_friends(node, current_date)
        num_adopted_friends = self.num_adopted_friends(node, current_date)
        if num_friends == 0:
            return 0
        return num_adopted_friends / num_friends

    def sentiment(self, n, current_date):
        if self.fake_sentiment:
            # fake sentiment
            if (n, current_date) not in self.sentiment_data:
                self.sentiment_data[(n, current_date)] = random.uniform(-1, 1)
            return self.sentiment_data[(n, current_date)]
        else:
            # real sentiment
            neighbors = self.adopted_friends(n, current_date)
            if len(neighbors) == 0:
                return 0
            sentiment_value = 0
            step = self.date_to_step(current_date)
            for neighbor in neighbors:
                sentiment_value += self.sentiment_data[neighbor][step]
            # if len(neighbors) >= 2:
            #     print("value {} friends {}: {}".format(sentiment_value / len(neighbors), len(neighbors), [self.sentiment_data[n][step] for n in neighbors]))
            return sentiment_value / len(neighbors)

    def date_to_step(self, timestamp):
        if timestamp < self.start_date:
            return 0
        return (timestamp - self.start_date) // self.intervals

    def average_num_of_adopted_neighbor_per_step(self):
        neighbors_per_step = self.get_number_of_adopted_neighbors_per_step()
        average_neighbors_per_step = []
        for neighbors in neighbors_per_step:
            if len(neighbors) == 0:
                average_neighbors_per_step.append(0)
            else:
                average_neighbors_per_step.append(sum(neighbors) // len(neighbors))
        return average_neighbors_per_step

    def get_number_of_adopted_neighbors_per_step(self):
        # return
        # [
        #       [neighbors_num1, neighbors2, ... ],             Step 1
        #       [],                                             Step 2
        #       [],                                             Step 3
        #       ...
        # ]

        step = 0
        neighbors = [[] for _ in range(self.stop_step+1)]
        non_adopted = self.users()
        current_date = self.start_date

        while step <= self.stop_step:
            non_adopted_next_step = []
            for n in non_adopted:
                neighbors[step].append(self.num_adopted_friends(n, current_date))
                if self.user_adopted_time(n) > current_date:
                    non_adopted_next_step.append(n)

            non_adopted = non_adopted_next_step
            current_date += self.intervals
            step += 1
        return neighbors

    def get_number_of_neighbors_per_step(self):
        # return
        # [
        #       [neighbors_num1, neighbors2, ... ],             Step 1
        #       [],                                             Step 2
        #       [],                                             Step 3
        #       ...
        # ]

        step = 0
        neighbors = [[] for _ in range(self.stop_step+1)]
        non_adopted = self.users()
        current_date = self.start_date

        while step <= self.stop_step:
            non_adopted_next_step = []
            for n in non_adopted:
                neighbors[step].append(len(self.friends(n, current_date)))
                if self.user_adopted_time(n) > current_date:
                    non_adopted_next_step.append(n)

            non_adopted = non_adopted_next_step
            current_date += self.intervals
            step += 1
        return neighbors