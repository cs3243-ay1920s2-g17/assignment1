import os
import sys
from itertools import chain
from Queue import Queue
from copy import deepcopy


class Node:
    def __init__(self, state, parent = None, move = None):
        self.state = state
        self.parent = parent

        if parent is None:
            self.depth = 0
            self.moves = list()
        else:
            self.depth = parent.depth + 1
            self.moves = list(parent.moves)
            self.moves.append(move)

    def succ(self):
        succs = Queue()

        for m in self.state.actions:
            transition = self.state.do_move(m)

            if transition.empty_pos != self.state.empty_pos:
                succs.put(Node(transition, self, m))

        return succs

    def is_goal_state(self):
        return self.state.check_goal_state()

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.state = init_state
        self.goal_state = goal_state
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        for x in range(n):
            for y in range(n):
                if self.init_state[x][y] == 0:
                    self.empty_pos = (x, y)

    def do_move(self, move):
        if move == "UP":
            return self.up()
        if move == "DOWN":
            return self.down()
        if move == "LEFT":
            return self.left()
        if move == "RIGHT":
            return self.right()

    def swap(self, (x1, y1), (x2, y2)):
        temp = self.state[x1][y1]
        self.state[x1][y1] = self.state[x2][y2]
        self.state[x2][y2] = temp

    def down(self):
        if (self.empty_pos[0] != 0):
            t = deepcopy(self)
            pos = (t.empty_pos[0] - 1, t.empty_pos[1])
            t.swap(pos, t.empty_pos)
            t.empty_pos = pos

            return t
        else:
            return self

    def up(self):
        if (self.empty_pos[0] != n - 1):
            t = deepcopy(self)
            pos = (t.empty_pos[0] + 1 , t.empty_pos[1])
            t.swap(pos, t.empty_pos)
            t.empty_pos = pos

            return t
        else:
            return self

    def right(self):
        if (self.empty_pos[1] != 0):
            t = deepcopy(self)
            pos = (t.empty_pos[0] , t.empty_pos[1] - 1)
            t.swap(pos, t.empty_pos)
            t.empty_pos = pos

            return t
        else:
            return self

    def left(self):
        if (self.empty_pos[1] != n - 1):
            t = deepcopy(self)
            pos = (t.empty_pos[0] , t.empty_pos[1] + 1)
            t.swap(pos, t.empty_pos)
            t.empty_pos = pos

            return t
        else:
            return self

    def check_goal_state(self):
        return self.state == self.goal_state

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

    def depth_limited(self, node, depth):
        if node.is_goal_state():
            return node
        if node.depth >= depth:
            return None

        succs = node.succ()

        while not succs.empty():
            result = self.depth_limited(succs.get(), depth)
            if result is not None:
                return result

    def solve(self):
        if not self.is_solvable():
            return ["UNSOLVABLE"]

        depth = 0
        goal_node = None

        while goal_node == None:
            goal_node = self.depth_limited(Node(self), depth)
            depth += 1

        return goal_node.moves

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







