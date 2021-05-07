'''
Structure written by: Nils Napp
Modified & Solution by: Jiwon Choi (F18 HW script)
'''
import numpy as np
from markov import *

# Actions of Maze problem
actions = ['up', 'left', 'down', 'right', 'stop']

class MDPMaze:
    def __init__(self, maze, stateReward):

        self.maze = maze
        self.stateReward = stateReward
        self.stateSize = maze.stateSize
        self.stateReward.resize(self.stateSize)

        self.eps = 0.30
        self.gamma = 0.9
        self.rewardM = np.ones(self.stateSize) * (-1)

        # place holders for computing transition matrices
        self.Aup = None
        self.Aleft = None
        self.Adown = None
        self.Aright = None
        self.Astop = None

        # computeTransitionMatrices function should compute self.Aup, self.Aleft, self.Adown, self.Aright and self.Astop
        # update the 5 matrices inside computeTransitionMatrices()
        self.computeTransitionMatrices()

        self.value = np.zeros(self.stateSize)
        self.policy = []

        # You can use this to construct the noisy matrices

    def ARandomWalk(self):
        A = np.zeros((self.stateSize, self.stateSize))

        for col in range(self.stateSize):
            nbrs = self.maze.nbrList(col)
            p = 1 / (len(nbrs) + 1)
            A[col, col] = p
            for r in nbrs:
                A[r, col] = p
        return A

    def computeTransitionMatrices(self):
        Arandom = self.ARandomWalk()

        Aup_perfect = np.zeros((self.stateSize, self.stateSize))
        Aleft_perfect = np.zeros((self.stateSize, self.stateSize))
        Adown_perfect = np.zeros((self.stateSize, self.stateSize))
        Aright_perfect = np.zeros((self.stateSize, self.stateSize))
        Astop_perfect = np.zeros((self.stateSize, self.stateSize))

        for i in range(0, self.stateSize):
            action = self.maze.actionList(i)
            position = self.maze.nbrList(i)

            # Aup_perfect
            if 'U' not in action:
                r, c = self.maze.state2coord(i)
                cord = self.maze.coord2state((r, c))
                Aup_perfect[cord][i] = 1
            else:
                p = action.index('U')
                Aup_perfect[position[p]][i] = 1

            # Aleft_perfect
            if 'L' not in action:
                r, c = self.maze.state2coord(i)
                cord = self.maze.coord2state((r, c))
                Aleft_perfect[cord][i] = 1
            else:
                p = action.index('L')
                Aleft_perfect[position[p]][i] = 1

            # Adown_perfect
            if 'D' not in action:
                r, c = self.maze.state2coord(i)
                cord = self.maze.coord2state((r, c))
                Adown_perfect[cord][i] = 1
            else:
                p = action.index('D')
                Adown_perfect[position[p]][i] = 1

            # Aright_perfect
            if 'R' not in action:
                r, c = self.maze.state2coord(i)
                cord = self.maze.coord2state((r, c))
                Aright_perfect[cord][i] = 1
            else:
                p = action.index('R')
                Aright_perfect[position[p]][i] = 1

            # Astop_perfect
            r, c = self.maze.state2coord(i)
            cord = self.maze.coord2state((r, c))
            Astop_perfect[cord][i] = 1

        self.Aup = ((1 - self.eps) * Aup_perfect) + (self.eps * Arandom)
        self.Aleft = ((1 - self.eps) * Aleft_perfect) + (self.eps * Arandom)
        self.Adown = ((1 - self.eps) * Adown_perfect) + (self.eps * Arandom)
        self.Aright = ((1 - self.eps) * Aright_perfect) + (self.eps * Arandom)
        self.Astop = Astop_perfect

    def valIter(self):
        gamma = self.gamma
        reward = self.stateReward
        size = self.stateSize
        Right = np.zeros(size)
        Left = np.zeros(size)
        Up = np.zeros(size)
        Down = np.zeros(size)
        Stop = np.zeros(size)
        for i in range(size):
            Right[i] = reward[i]-1+gamma*np.dot(self.Aright[:,i],self.value);
            Left[i] = reward[i]-1+gamma*np.dot(self.Aleft[:,i],self.value);
            Up[i] = reward[i]-1+gamma*np.dot(self.Aup[:,i],self.value);
            Down[i] = reward[i]-1+gamma*np.dot(self.Adown[:,i],self.value);
            Stop[i] = reward[i]+gamma*np.dot(self.Astop[:,i],self.value);
        Value = np.amax(np.array([Right,Left,Up,Down,Stop]), axis = 0);
        self.value = Value
        return self.value
  
    def polIter(self):
        gamma = self.gamma
        reward = self.stateReward
        size = self.stateSize
        Right = np.zeros(size)
        Left = np.zeros(size)
        Up = np.zeros(size)
        Down = np.zeros(size)
        Stop = np.zeros(size)
        self.policy = []
        for i in range(size):
            Right[i] = reward[i]-1+gamma*np.dot(self.Aright[:,i],self.value);
            Left[i] = reward[i]-1+gamma*np.dot(self.Aleft[:,i],self.value);
            Up[i] = reward[i]-1+gamma*np.dot(self.Aup[:,i],self.value);
            Down[i] = reward[i]-1+gamma*np.dot(self.Adown[:,i],self.value);
            Stop[i] = reward[i]+gamma*np.dot(self.Astop[:,i],self.value);
        arg_Value = np.argmax(np.array([Right,Left,Up,Down,Stop]), axis = 0);
        direction = ['right', 'left', 'up', 'down', 'stop']
        for i in arg_Value:
            self.policy.append(direction[i])
        return self.policy

# ------------------------------------------------------------- #
if __name__ == "__main__":
    myMaze = maze(np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]))

    stateReward = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 100, 0, 0, 0, 0, 0],
        [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000]])

    mdp = MDPMaze(myMaze, stateReward)

    iterCount = 100
    printSkip = 10

    for i in range(iterCount):
        mdp.valIter()
        mdp.polIter()
        if np.mod(i, printSkip) == 0:
            print("Iteration ", i)
            print (mdp.policy)
            print (mdp.value)
