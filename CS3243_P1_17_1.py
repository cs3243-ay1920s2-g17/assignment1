import os
import sys
from itertools import chain
from collections import deque

# Iterative Deepening Search (IDS)

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


    def find_empty_pos(self, state):
        for x in range(n):
            for y in range(n):
                if state[x][y] == 0:
                    return (x, y)

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
    def __init__(self, init_state, goal_state):
        global n
        global max_num
        n = len(init_state[0])
        max_num = n ** 2 - 1
        self.init_state = init_state
        self.state = init_state
        self.goal_state = goal_state
        self.total_nodes = 1
        self.total_visited = 0
        self.max_frontier = 0
        self.depth = 0
        self.visited = {}
        self.frontier_node = []
        self.move_dict = {}

    def is_goal_state(self, node):
        return node.state == self.goal_state

    def is_solvable(self):
        flat_list = list(chain.from_iterable(self.init_state))
        num_inversions = 0

        for i in range(max_num):
            current = flat_list[i]

            for j in range(i + 1, max_num + 1):
                next = flat_list[j]

                if current > next and next != 0:
                    num_inversions += 1

        if n % 2 != 0 and num_inversions % 2 == 0:
            return True
        elif n % 2 == 0:
            row_with_blank = n - flat_list.index(0) // n

            return (row_with_blank % 2 == 0) == (num_inversions % 2 != 0)
        else:
            return False

    def succ(self, node, frontier):
        succs = deque()
        node_str = str(node.state)



        self.total_visited += 1
        frontier -= 1

        for m in node.actions:
            transition, t_empty = node.do_move(m)
            transition_str = str(transition)
            transition_depth = node.depth + 1

            if transition_str not in self.visited or transition_depth < self.visited[transition_str]:

                self.visited[transition_str] = transition_depth
                self.total_nodes += 1
                transition_depth = node.depth + 1
                transition_str = str(transition)
                self.move_dict[transition_str] = (node_str, m)
                succs.append(Node(transition, t_empty, transition_depth))
                frontier += 1


        return succs , frontier



    def depth_limited(self, node, depth, frontier):
        if self.is_goal_state(node):
            return node
        if node.depth >= depth:
            return None

        self.visited[str(node)] = 0
        succs, frontier = self.succ(node, frontier)
        self.max_frontier = max(self.max_frontier, frontier)

        while succs:
           result = self.depth_limited(succs.popleft(), depth, frontier)

           if result is not None:
                return result

        return None

    def solve(self):
        if not self.is_solvable():
            return ["UNSOLVABLE"]

        goal_node = None

        while goal_node is None:
            goal_node = self.depth_limited(Node(self.init_state), self.depth, 1)

            if goal_node is not None:
                break

            # reset statistics
            self.visited = {}
            self.total_nodes = 1
            self.move_dict = {}

            self.depth += 1

            # print self.depth

        # print "out"
        solution = deque()
        init_str = str(self.init_state)
        current_str = str(goal_node.state)
        while current_str != init_str:
            current_str, move = self.move_dict[current_str]
            # print current_str, move
            solution.appendleft(move)

        print "Total number of nodes generated: " + str(self.total_nodes)
        print "Total number of nodes explored: " + str(self.total_visited)
        print "Maximum number of nodes in frontier: " + str(self.max_frontier)
        print "Solution depth: " + str(self.depth)
        return solution

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]


    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







