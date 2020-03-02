import os
import sys
from itertools import chain
import heapq

# A* Search using Manhattan Distance + Linear Conflict heuristics

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
        return self.manhattan_dist_linear_conflict(state) + self.depth + 1

    def manhattan_dist_linear_conflict(self, state):
        dist = 0
        rows = [[0 for i in range(n)] for j in range(n)]
        columns = [[0 for i in range(n)] for j in range(n)]

        for x in range(n):
            for y in range(n):
                current_tile = state[x][y]

                if current_tile != 0:
                    current_tile -= 1
                    x_diff = abs(x - current_tile // n)
                    y_diff = abs(y - current_tile % n)
                    dist += x_diff + y_diff
                    current_tile += 1
                    
                    # correct column
                    if y_diff == 0:
                        columns[y][x] = current_tile

                    # correct row
                    if x_diff == 0:
                        rows[x][y] = current_tile

        num_conflict = 0

        for i in range(n):
            current_row = rows[i]
            current_column = columns[i]

            for j in range(n):
                r_value = current_row[j]
                c_value = current_column[j]

                for k in range(j + 1, n):
                    next_r_value = current_row[k]
                    next_c_value = current_column[k]

                    if r_value > next_r_value and next_r_value != 0:
                        num_conflict += 1

                    if c_value > next_c_value and next_c_value != 0:
                        num_conflict += 1
                        
        return dist + 2 * num_conflict

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
        self.init_state = init_state
        self.state = init_state
        self.goal_state = goal_state
        self.visited = set()
        self.frontier_node = []
        self.frontier_cost_set = set()
        self.move_dict = {}
        self.total_nodes = 1
        self.total_visited = 0
        self.max_frontier = 0
        self.depth = 0
 
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
        node_str = str(node.state)
        self.visited.add(node_str)
        self.total_visited += 1
        frontier -= 1

        for m in node.actions:
            transition, t_empty = node.do_move(m)
            transition_depth = node.depth + 1
            transition_str = str(transition)
            transition_cost = node.est_cost(transition)
            transition_cost_str = str(transition_cost) + str(transition)

            if t_empty != node.empty_pos:
                self.total_nodes += 1

            if transition_cost_str not in self.frontier_cost_set and transition_str not in self.visited:
                self.frontier_cost_set.add(transition_cost_str)
                self.move_dict[transition_str] = (node_str, m)
                heapq.heappush(self.frontier_node, (transition_cost, Node(transition, t_empty, transition_depth)))
                frontier += 1

        return frontier

    def a_star(self, node, frontier):
        while True:
            if self.is_goal_state(node):
                return node

            frontier = self.succ(node, frontier)
            self.max_frontier = max(self.max_frontier, frontier)
            cost, node = heapq.heappop(self.frontier_node)
            self.frontier_cost_set.remove(str(cost) + str(node.state))

    def solve(self):
        if not self.is_solvable():
            return ["UNSOLVABLE"]

        goal_node = self.a_star(Node(self.init_state), 1)
       
        print "Total number of nodes generated: " + str(self.total_nodes)
        print "Total number of nodes explored: " + str(self.total_visited)
        print "Maximum number of nodes in frontier: " + str(self.max_frontier)
        print "Solution depth: " + str(goal_node.depth)
        
        solution = []
        init_str = str(self.init_state)
        current_str = str(goal_node.state)

        # recursion?
        while current_str != init_str:
            current_str, move = self.move_dict[current_str]
            solution.append(move)

        return solution[::-1]

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







