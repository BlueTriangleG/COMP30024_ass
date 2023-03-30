from .functions import move
import math

class node:
    # all possible move direction
    move_direction = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1)]

    # initialize the node by entering the table, parent, action and cost
    def __init__(self, table: dict[tuple, tuple], parent=None, action=None, cost=0):
        self.parent = parent
        self.children = []
        self.blue_node = []
        self.red_node = []
        self.table = table
        self.lest_straight_distant = 1000
        # number of cost used to reach this step
        self.cost = cost
        self.fx = 0
        # action is a list of tuple, append during the expansion
        self.action = action
        # move the token to get the new table
        self.move_token()
        # get the token and calculate the least cost on current situation
        self.get_token()
        self.calculate_cost()

    # move the token according to the least action
    def move_token(self):
        # if the action is None, do nothing
        if self.action is None:
            self.action = []
        else:
            # get the least action
            least_action = self.action[-1]
            # move the token
            self.table = move(least_action, self.table)

    # put the Blue token and Red token into a list
    def get_token(self):
        for key, value in self.table.items():
            if value[0] == "b":
                self.blue_node.append(key)
            elif value[0] == "r":
                self.red_node.append(key)

    # check if the goal is reached
    def goal(self):
        if len(self.blue_node) == 0:
            return True
        else:
            return False

    # calculate the f(X) = g(X) + h(X)
    def calculate_cost(self):
        # calculate the h(X) use Manhattan distance
        self.least_straight_distant()
        # calculate the f(X)
        self.fx = self.cost + self.lest_straight_distant

    # calculate the least straight distance between red token and blue token
    def least_straight_distant(self):
        current_distance = 0
        spread_distance = 0
        for red in self.red_node:
            spread_distance = self.table[red][1]
            for blue in self.blue_node:
                # as the position 7 is connected to 0, so we need to ensure the distance is the least
                # I create new position by adding 7 and reduce 7 to the position to let the distance be the least
                current_distance = math.sqrt(min(abs(blue[0]+7-red[0]), abs(blue[0]-red[0]), abs(blue[0]-7-red[0]))**2 + \
                                   min(abs(blue[1]+7-red[1]), abs(blue[1]-red[1]), abs(blue[1]-7-red[1]))**2)/spread_distance
            self.lest_straight_distant += current_distance
            #if current_distance < self.lest_straight_distant:
               # self.lest_straight_distant = current_distance

    # expand the node and create children by using detect all the red token's move cost to other blue token
    # for every red token, enter one possible movement and calculate the cost and create a node.
    def expand(self):
        # for every red token
        for red in self.red_node:
            # for every possible move
            for move in self.move_direction:
                new_action = self.action.copy()
                new_action.append((red[0], red[1], move[0], move[1]))
                # create a new node
                # copy the table
                new_table = self.table.copy()
                new_node = node(new_table, self, new_action, self.cost + 1)
                # add the new node to the children
                self.add_child(new_node)

    # define compare function
    def __lt__(self, other):
        return self.fx < other.fx

    def add_child(self, child):
        self.children.append(child)

    # get table
    def get_table(self):
        return self.table

    # get action
    def get_action(self):
        return self.action

    # get children
    def get_children(self):
        return self.children

    # get cost
    def get_cost(self):
        return self.cost
