# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import heapq
from .node import node
from .functions import *
from .utils import render_board


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    """
    input = state of the board
    goal -> no blue cells. working by a function.
    """
    # create a priority queue
    priority_queue = []
    # create the first node
    first_node = node(input)
    # push the first node into the priority queue
    heapq.heappush(priority_queue, first_node)
    # start search
    current_node = first_node
    print(render_board(input, ansi=True))
    numbers = 0
    n = 1
    print(numbers)
    while True:
        # check if the priority queue is empty
        # if empty, return nothing
        if(numbers == 1000*n):
            print(numbers)
            n += 1
        numbers += 1
        if len(priority_queue) == 0:
            print(render_board(input, ansi=True))
            return []
        # get the first node
        current_node = heapq.heappop(priority_queue)
        # check if the goal is reached
        if current_node.goal():
            for action in current_node.get_action():
                move(action, first_node.get_table())
                print(render_board(first_node.get_table(), ansi=True))
            print(numbers)
            return current_node.get_action()
        # expand the node
        current_node.expand()
        # add the children to the priority queue
        for child in current_node.get_children():
            heapq.heappush(priority_queue, child)

    # The render_board function is useful for debugging -- it will print out a
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
