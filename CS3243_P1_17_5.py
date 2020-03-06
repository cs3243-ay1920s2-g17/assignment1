'''
Experiment file
'''

import random
import CS3243_P1_17_1 #uninformed
import CS3243_P1_17_2 #misplaced tiles
import CS3243_P1_17_3 #manhattan
import CS3243_P1_17_4 #linear conflict
import timeit
'''
#undo multiline comment to utilize run() function. It returns a list of 5 randomly selected initial state with specified depth from goal state

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
'''

# TESTING FUNCTIONS
def generate_goal_state(n, max_num):
    goal_state = [[0 for i in range(n)] for j in range(n)]
    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0
    return goal_state

def run_method(i, init_state, goal_state):
    # code you want to evaluate
    start_time = timeit.default_timer()
    if i == 0:
        print("Using Uninformed Search (Iterative Deepening Search)")
        puzzle = CS3243_P1_17_1.Puzzle(init_state, goal_state)
        puzzle.solve()
    elif i == 1:
        print("Using Informed Search (Hamming Distance)")
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
    elapsed = timeit.default_timer() - start_time
    print("Search Time: " + str(elapsed))

# PRE-COMPUTED initial states for n = 3, depth 20
n3d20i1 = [[8, 7, 2], [4, 3, 6], [5, 1, 0]]
n3d20i2 = [[3, 6, 8], [4, 0, 1], [7, 5, 2]]
n3d20i3 = [[0, 3, 1], [4, 6, 7], [5, 2, 8]]
n3d20i4 = [[1, 5, 3], [7, 4, 8], [2, 6, 0]]
n3d20i5 = [[5, 1, 6], [4, 0, 7], [2, 8, 3]]

# PRE-COMPUTED initial states for n = 3, depth 25
n3d25i1 = [[7, 4, 8], [0, 2, 5], [3, 1, 6]]
n3d25i2 = [[1, 7, 5], [0, 2, 6], [8, 3, 4]]
n3d25i3 = [[6, 4, 8], [0, 1, 7], [3, 5, 2]]
n3d25i4 = [[6, 5, 2], [0, 8, 4], [1, 3, 7]]
n3d25i5 = [[8, 5, 1], [0, 6, 7], [3, 2, 4]]

# Test both uniformed and all informed
def test_n3():
    n = 3
    max_num = n ** 2 - 1
    goal_state = generate_goal_state(n, max_num)

    list_of_init_states_depth20 = []
    list_of_init_states_depth20.append(n3d20i1)
    list_of_init_states_depth20.append(n3d20i2)
    list_of_init_states_depth20.append(n3d20i3)
    list_of_init_states_depth20.append(n3d20i4)
    list_of_init_states_depth20.append(n3d20i5)

    list_of_init_states_depth25 = []
    list_of_init_states_depth25.append(n3d25i1)
    list_of_init_states_depth25.append(n3d25i2)
    list_of_init_states_depth25.append(n3d25i3)
    list_of_init_states_depth25.append(n3d25i4)
    list_of_init_states_depth25.append(n3d25i5)

    counter = 1

    # for n = 3, depth = 20
    for i in range(len(list_of_init_states_depth20)):
        init_state = list_of_init_states_depth20[i]
        print ("+" * 86)
        print("+ Test case: {0}; Initial state: {1}; Expected depth: {2} +".format(str(counter), str(init_state), str(20)))
        print ("+" * 86)
        counter += 1
        for j in range(4):
            run_method(j, init_state, goal_state)
            print("")

    # for n = 3, depth = 25
    for i in range(len(list_of_init_states_depth25)):
        init_state = list_of_init_states_depth25[i]
        print ("+" * 86)
        print("+ Test case: {0}; Initial state: {1}; Expected depth: {2} +".format(str(counter), str(init_state), str(25)))
        print ("+" * 86)
        counter += 1
        for j in range(4):
            run_method(j, init_state, goal_state)
            print("")

# PRE-COMPUTED initial states for n = 4, depth 20
n4d20i1 = [[1, 13, 2, 4], [6, 3, 7, 8], [5, 11, 12, 15], [10, 9, 14, 0]]
n4d20i2 = [[0, 1, 2, 4], [9, 5, 3, 8], [13, 6, 7, 10], [11, 15, 14, 12]]
n4d20i3 = [[5, 10, 1, 4], [6, 2, 12, 3], [9, 7, 11, 8], [13, 14, 15, 0]]
n4d20i4 = [[2, 6, 3, 4], [1, 7, 15, 12], [0, 5, 9, 8], [13, 10, 14, 11]]
n4d20i5 = [[9, 5, 0, 3], [1, 11, 7, 4], [6, 2, 10, 8], [13, 14, 15, 12]]

# Test only for Manhattan & Linear Conflict
def test_n4():
    n = 4
    max_num = n ** 2 - 1
    goal_state = generate_goal_state(n, max_num)

    list_of_init_states_depth20 = []
    list_of_init_states_depth20.append(n4d20i1)
    list_of_init_states_depth20.append(n4d20i2)
    list_of_init_states_depth20.append(n4d20i3)
    list_of_init_states_depth20.append(n4d20i4)
    list_of_init_states_depth20.append(n4d20i5)

    counter = 11

    # for n = 4, depth = 20
    for i in range(len(list_of_init_states_depth20)):
        init_state = list_of_init_states_depth20[i] # returns a node
        print ("+" * 116)
        print("+ Test case: {0}; Initial state: {1}; Expected depth: {2} +".format(str(counter), str(init_state), str(20)))
        print ("+" * 116)
        counter += 1
        for j in range(2, 4):
            run_method(j, init_state, goal_state)
            print("")

# PRE-COMPUTED initial states for n = 5, depth 15
n5d15i1 = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [12, 13, 14, 0, 19], [11, 16, 17, 15, 24], [21, 22, 18, 23, 20]]
n5d15i2 = [[1, 2, 3, 4, 5], [6, 7, 9, 13, 10], [11, 0, 8, 14, 15], [16, 12, 22, 18, 20], [21, 23, 17, 19, 24]]
n5d15i3 = [[1, 2, 3, 9, 4], [6, 7, 8, 14, 5], [17, 16, 12, 13, 10], [11, 22, 18, 19, 15], [21, 0, 23, 24, 20]]
n5d15i4 = [[6, 1, 2, 4, 5], [0, 7, 3, 8, 10], [11, 13, 19, 9, 14], [16, 12, 17, 18, 15], [21, 22, 23, 24, 20]]
n5d15i5 = [[1, 2, 3, 4, 5], [6, 7, 13, 8, 14], [11, 12, 18, 10, 15], [16, 17, 23, 9, 19], [21, 0, 22, 24, 20]]

# Test only for Manhattan & Linear Conflict
def test_n5():
    n = 5
    max_num = n ** 2 - 1
    goal_state = generate_goal_state(n, max_num)

    list_of_init_states_depth15 = []
    list_of_init_states_depth15.append(n5d15i1)
    list_of_init_states_depth15.append(n5d15i2)
    list_of_init_states_depth15.append(n5d15i3)
    list_of_init_states_depth15.append(n5d15i4)
    list_of_init_states_depth15.append(n5d15i5)

    counter = 16

    # for n = 5, depth = 15
    for i in range(len(list_of_init_states_depth15)):
        init_state = list_of_init_states_depth15[i] # returns a node
        print ("+" * 154)
        print("+ Test case: {0}; Initial state: {1}; Expected depth: {2} +".format(str(counter), str(init_state), str(15)))
        print ("+" * 154)
        counter += 1
        for j in range(2, 4):
            run_method(j, init_state, goal_state)
            print("")

# current runtime: MAX 3min
test_n3()
test_n4()
test_n5()




