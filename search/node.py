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
        self.least_manhattan_distant = 1000
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
        # calculate the h(X) use straight distance h(x)2
        self.least_straight_distant()
        # calculate the number of blue token h(x)1
        blue_number = self.blue_token_number()
        # calculate the f(X)
        self.fx = self.cost + self.least_manhattan_distant + blue_number
    # calculate the h(x)
    #def heuristic(self):


    # calculate the least straight distance between red token and blue token
    def least_straight_distant(self):
        blue_manhattan_distance = 1000
        current_distance = 0
        current_distance_blue = 1000
        current_manhattan_distance = 1000
        # get the least distance between red token and blue token
        if len(self.blue_node) != 0:
            for red in self.red_node:
                spread_distance = self.table[red][1]
                for blue in self.blue_node:
                    # as the position 7 is connected to 0, so we need to ensure the distance is the least
                    # I create new position by adding 7 and reduce 7 to the position to let the distance be the least
                    #blue_distance = math.sqrt(min(abs(blue[0]+7-red[0]), abs(blue[0]-red[0]), abs(blue[0]-7-red[0]))**2 + \
                    #                   min(abs(blue[1]+7-red[1]), abs(blue[1]-red[1]), abs(blue[1]-7-red[1]))**2)/spread_distance
                    blue_manhattan_distance = self.least_manhattan_distant_calculate(red, blue)/spread_distance
                    #if blue_distance < current_manhattan_distance:
                    #    current_distance_blue = blue_distance
                    if blue_manhattan_distance < current_distance_blue:
                        current_distance_blue = blue_manhattan_distance
                # get the least distance between red token and blue token
                #if current_distance_blue < self.lest_straight_distant:
                #    self.lest_straight_distant = current_distance_blue
                if blue_manhattan_distance< self.least_manhattan_distant:
                    self.least_manhattan_distant = blue_manhattan_distance
        else:
            self.lest_straight_distant = 0
            self.least_manhattan_distant = 0

    # calculate the least manhattan distance between red token and blue token
    def axial_to_cube(self,r, q):
        x = r
        z = q
        y = -x - z
        return x, y, z

    def cube_distance(self,a, b):
        ax, ay, az = a
        bx, by, bz = b
        return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) // 2
    def least_manhattan_distant_calculate(self,red, blue):
        cube_coord1 = self.axial_to_cube(red[0], red[1])
        cube_coord2 = self.axial_to_cube(blue[0], blue[1])
        return self.cube_distance(cube_coord1, cube_coord2)


    # calculate the number of blue token
    def blue_token_number(self):
        blue_number = len(self.blue_node)
        if blue_number == 0:
            return 1
        return blue_number

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
