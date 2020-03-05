'''
Experiment file
'''

import random 
import CS3243_P1_17_1 #uninformed
import CS3243_P1_17_2 #misplaced tiles
import CS3243_P1_17_3 #manhattan
import CS3243_P1_17_4 #linear conflict

# returns a list of 5 randomly selected initial state with specified depth from goal
def run(depth, number):
    global n
    n = number
    max_num = n ** 2 - 1
    init_state = [[0 for i in range(n)] for j in range(n)]
    for i in range(1, max_num + 1):
        init_state[(i - 1) // n][(i - 1) % n ] = i

    init_state[n - 1][n - 1] = 0
    goal_depth = depth
    puzzle = Puzzle(goal_depth)
    result = puzzle.bfs(Node(init_state))
    return result

# Node and Puzzle class to generate random initial states with a specific depth from the goal state
class Node:
    def __init__(self, state, empty_pos = None, depth = 0):
        self.state = state
        self.depth = depth
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        if empty_pos is None:
            self.empty_pos = self.find_empty_pos(self.state)
        else:
            self.empty_pos = empty_pos

    def find_empty_pos(self, state):
        for x in range(n):
            for y in range(n):
                if state[x][y] == 0:
                    return (x, y)

    def est_cost(self, state):
        return self.manhattan_dist(state) + self.depth + 1

    def manhattan_dist(self, state):
        dist = 0

        for x in range(n):
            for y in range(n):
                current_tile = state[x][y]

                if current_tile != 0:
                    current_tile -= 1
                    x_diff = abs(x - current_tile // n)
                    y_diff = abs(y - current_tile % n)
                    dist += x_diff + y_diff

        return dist

    def do_move(self, move):
        if move == "UP":
            return self.up()
        if move == "DOWN":
            return self.down()
        if move == "LEFT":
            return self.left()
        if move == "RIGHT":
            return self.right()

    def swap(self, state, (x1, y1), (x2, y2)):
        temp = state[x1][y1]
        state[x1][y1] = state[x2][y2]
        state[x2][y2] = temp

    def down(self):
        empty = self.empty_pos

        if (empty[0] != 0):
            t = [row[:] for row in self.state]
            pos = (empty[0] - 1, empty[1])
            self.swap(t, pos, empty)

            return t, pos
        else:
            return self.state, empty

    def up(self):
        empty = self.empty_pos

        if (empty[0] != n - 1):
            t = [row[:] for row in self.state]
            pos = (empty[0] + 1 , empty[1])
            self.swap(t, pos, empty)

            return t, pos
        else:
            return self.state, empty

    def right(self):
        empty = self.empty_pos

        if (empty[1] != 0):
            t = [row[:] for row in self.state]
            pos = (empty[0] , empty[1] - 1)
            self.swap(t, pos, empty)

            return t, pos
        else:
            return self.state, empty

    def left(self):
        empty = self.empty_pos

        if (empty[1] != n - 1):
            t = [row[:] for row in self.state]
            pos = (empty[0] , empty[1] + 1)
            self.swap(t, pos, empty)

            return t, pos
        else:
            return self.state, empty

class Puzzle(object):
    def __init__(self, depth):
        self.goal_depth = depth
        self.frontier = [] # a list containing nodes
        self.frontier_set = set()
        self.visited_states = set() # a set of unique states visited already

    def succ(self, node):
        self.frontier.remove(node)
        self.frontier_set.discard(str(node.state))
        self.visited_states.add(str(node.state))

        for m in node.actions:
            transition, t_empty = node.do_move(m)
            neighbour = Node(transition, t_empty, node.depth + 1)
            neighbour_str = str(neighbour.state)

            if (t_empty != node.empty_pos) and (str(transition) not in self.visited_states) and (str(neighbour.state) not in self.frontier_set):
                self.frontier_set.add(neighbour_str)
                self.frontier.append(neighbour)

    def bfs(self, node): 
        self.frontier.append(node)
        self.frontier_set.add(str(node))
        while True:
            if (node.depth == self.goal_depth):
                length = len(self.frontier)
                random_states = []

                if (length <= 5):
                    for i in range(length):
                         random_states.append(self.frontier[i])
                    return random_states

                while len(random_states) != 5:
                    index = random.randint(0, length - 1)
                    state = self.frontier[index]

                    if state not in random_states:
                        random_states.append(state)

                return random_states

            self.succ(node)
            node = self.frontier[0]

# TESTING FUNCTIONS 
def generate_goal_state(n, max_num):
    goal_state = [[0 for i in range(n)] for j in range(n)]
    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0
    return goal_state

def run_method(i, init_state, goal_state):
    if i == 0:
        print("Using Uninformed Search (IDS)")
        puzzle = CS3243_P1_17_1.Puzzle(init_state, goal_state)
        puzzle.solve()
    elif i == 1:
        print("Using Informed Search (Misplaced Tiles)")
        puzzle = CS3243_P1_17_2.Puzzle(init_state, goal_state)
        puzzle.solve()
    elif i == 2:
        print("Using Informed Search (Manhattan Distance)")
        puzzle = CS3243_P1_17_3.Puzzle(init_state, goal_state)
        puzzle.solve()
    else: 
        print ("Using Informed Search (Linear Conflict)")
        puzzle = CS3243_P1_17_4.Puzzle(init_state, goal_state)
        puzzle.solve()

def test_n3():
    n = 3
    max_num = n ** 2 - 1
    goal_state = generate_goal_state(n, max_num)
    list_of_init_states_depth20 = run(20, 3)
    list_of_init_states_depth25 = run(25, 3)

    counter = 1

    # for n = 3, depth = 20
    for i in range(len(list_of_init_states_depth20)):
        init_state = list_of_init_states_depth20[i] 
        print("### N = 3; Test case {0}; Initial state: {1}; Expected depth: {2} ###;".format(str(counter), str(init_state.state), str(init_state.depth)))
        counter += 1
        for j in range(4):
            run_method(j, init_state.state, goal_state)
            print("")
    
    # for n = 3, depth = 25
    for i in range(len(list_of_init_states_depth25)):
        init_state = list_of_init_states_depth25[i] 
        print("### N = 3; Test case {0}; Initial state: {1}; Expected depth: {2}; ###".format(str(counter), str(init_state.state), str(init_state.depth)))
        counter += 1
        for j in range(4):
            run_method(j, init_state.state, goal_state)
            print("")

def test_n4():
    n = 4
    max_num = n ** 2 - 1
    goal_state = generate_goal_state(n, max_num)
    list_of_init_states_depth10 = run(10, 4)
    list_of_init_states_depth15 = run(15, 4)

    counter = 11

    # for n = 4, depth = 10
    for i in range(len(list_of_init_states_depth10)):
        init_state = list_of_init_states_depth10[i] # returns a node
        print("N = 4; Test case {0}; Initial state: {1}; Expected depth: {2};".format(str(counter), str(init_state.state), str(init_state.depth)))
        counter += 1
        for j in range(4):
            run_method(j, init_state.state, goal_state)
            print("")

    # for n = 4, depth = 15
    for i in range(len(list_of_init_states_depth15)):
        init_state = list_of_init_states_depth15[i] # returns a node
        print("### N = 4; Test case {0}; Initial state: {1}; Expected depth: {2} ###;".format(str(counter), str(init_state.state), str(init_state.depth)))
        counter += 1
        for j in range(4):
            run_method(j, init_state.state, goal_state)
            print("")

# current runtime: 5min 10sec
test_n3()
# might pre-populate the list instead of randomly generating...
test_n4()




