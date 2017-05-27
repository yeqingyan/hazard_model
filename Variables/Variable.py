# TODO For Swati, followed by X4Sentiment example, inherit this class and overwrite the get_covariates function
class Variable:
    def __init__(self, name):
        """
        Initilize varialbe
        :param name:            Variable name 
        """
        self.name = name

    def get_covariates(self, node, current_date, nonadopted_nodes):
        """        
        :param node:                Current node 
        :param current_date:        Current node
        :param nonadopted_nodes:    Current non-adopters at this step, this object is immutable for safety concern
        :return: 
        """
        assert False, "Override this function"