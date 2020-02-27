import os
import sys
from itertools import chain

import os
import sys
from Queue import Queue
from Queue import LifoQueue
from copy import deepcopy


class Node:
    def __init__(self, puzzle, parent=None, move=""):
        self.state = puzzle
        self.parent = parent
        self.depth = 0
        if parent is None:
            self.depth = 0
            self.moves = move
        else:
            self.depth = parent.depth+1
            self.moves = parent.moves + move

    def succ(self):
        succs = Queue()
        for m in self.state.actions:
            p = deepcopy(self.state)
            p.doMove(m)
            if p.zero is not self.state.zero:
                succs.put(Node(p, self, m))
        return succs

    def goalState(self):
        return self.state.isGoalState()

class TilePuzzle:
    def __init__(self, state, goalState, zero, size):
        self.state = state
        self.goalState = goalState
        self.actions = list(("U","D","L","R"))
        self.zero = zero
        self.size = size


    def doMove(self,move):
        if move=="U":
            self.up()
        if move=="D":
            self.down()
        if move=="L":
            self.left()
        if move=="R":
            self.right()

    def swap(self, (x1, y1), (x2, y2)):
        temp=self.state[x1][y1]
        self.state[x1][y1]=self.state[x2][y2]
        self.state[x2][y2]=temp

    def down(self):
        if (self.zero[0]!=0):
            self.swap((self.zero[0]-1,self.zero[1]),self.zero)
            self.zero=(self.zero[0]-1,self.zero[1])

    def up(self):
        if (self.zero[0]!=self.size-1):
            self.swap((self.zero[0]+1,self.zero[1]),self.zero)
            self.zero=(self.zero[0]+1,self.zero[1])

    def right(self):
        if (self.zero[1]!=0):
            self.swap((self.zero[0],self.zero[1]-1),self.zero)
            self.zero=(self.zero[0],self.zero[1]-1)


    def left(self):
        if (self.zero[1]!=self.size-1):
            self.swap((self.zero[0],self.zero[1]+1),self.zero)
            self.zero=(self.zero[0],self.zero[1]+1)

    def isGoalState(self):
        return self.state == self.goalState


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state

        for i in range(len(self.init_state)):
            for j in range(len(self.init_state[i])):
                if self.init_state[i][j] == 0:
                    print(i,j)
                    self.zero = (i,j)

        self.size = len(self.init_state)
        self.startNode = Node(TilePuzzle(self.init_state, self.goal_state, self.zero, self.size))

    def is_solvable(self):
        flat_list = list(chain.from_iterable(init_state))
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
            row_with_blank = n  - flat_list.index(0) // n
            return (row_with_blank % 2 == 0) == (num_inversions % 2 !=
            0)
        else:
            return False

    def depthLimited(self, depth):
        leaves = LifoQueue()
        leaves.put(self.startNode)
        while True:
            if leaves.empty():
                return None
            actual = leaves.get()
            if actual.goalState():
                return actual
            elif actual.depth is not depth:
                succ = actual.succ()
                while not succ.empty():
                    leaves.put(succ.get())

    def solve(self):
        if (not self.is_solvable()):
            return ""
        depth = 0
        result = None
        while result == None:
            result = self.depthLimited(depth)
            depth +=1
        return result.moves



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







