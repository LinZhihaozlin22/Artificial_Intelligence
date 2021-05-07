''' 
Structure written by: Nils Napp
Solution by: Jiwon Choi (F18 HW script)
'''
import heapq
import time
from slideproblem import * 
## you likely need to inport some more modules to do the serach

class Searches:
    def graph_bfs(self, problem):
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        n = Node(None,None,0,problem.initialState)
        s = State()
        p = problem
        if p.goalTest(n.state):
            return solution(n)
        frontier = [n]
        explored = set()
        while frontier:
            n = frontier.pop(0)
            l = p.applicable(n.state)
            explored.add(n.state.toTuple())
            for action in l :
                child = child_node(n,action,p)
                c = child.state.toTuple()
                if c not in explored and child not in frontier:
                    if p.goalTest(child.state):
                        return solution(child)
                    frontier.append(child)
        "*** YOUR CODE HERE ***"
        
        return "Fake return value"        

    def recursiveDL_DFS(self, lim, problem):
        n=Node(None,None,0,problem.initialState)
        return self.depthLimitedDFS(n,lim,problem)
        
    def depthLimitedDFS(self, n, lim, problem):
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        p = problem
        if p.goalTest(n.state) :
            return solution(n)
        elif lim == 0 :
            return None
        l = p.applicable(n.state)
        for child in l:
            result = self.depthLimitedDFS(child_node(n, child, p), lim-1, problem)
            if result != None:
                return result
        return "Fake return value" 

    def id_dfs(self,problem):
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        maxLim = 30
        d = 0
        while d <= maxLim:
            result = self.recursiveDL_DFS(d, problem)
            d += 1
            if result != None:
                return result
        return "Fake return value" 

    # START: DEFINED ALREADY
    def poseList(self,s):
        poses=list(range(s.boardSize*s.boardSize))
    
        for tile in range(s.boardSize*s.boardSize):
            for row in range(s.boardSize):
                for col in range(s.boardSize):
                    poses[s.board[row][col]]=[row,col]
        return poses
    
    def heuristic(self,s0,sf):
        pl0=self.poseList(s0)
        plf=self.poseList(sf)
    
        h=0
        for i in range(1,s0.boardSize*s0.boardSize):
            h += abs(pl0[i][0] - plf[i][0]) + abs( plf[i][1] - plf[i][1])       
        return h
    # END: DEFINED ALREADY
                
    def a_star_tree(self, problem: Problem) -> tuple:
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        p = problem
        n = Node(None,None,0,problem.initialState)
        ini = (0, n)
        frontier = [ini]        
        heapq.heapify(frontier)
        
        while frontier:
            z = heapq.heappop(frontier)
            u = z[1]
            if u.state == problem.goalState:
                return solution(u)
            
            act = Problem.applicable(self,u.state)
            chil = []
            for k in act:
                child = child_node(u,k,p)
                child.f = child.cost + self.heuristic(child.state, p.goalState)
                heapq.heappush(frontier,(child.f, child))
        return None

    def a_star_graph(self, problem: Problem) -> tuple:
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        p = problem
        n = Node(None,None,0,problem.initialState)
        ini = (0, n)
        frontier = [ini]        
        heapq.heapify(frontier)
        exp = set()
        while frontier:
            z = heapq.heappop(frontier)
            u = z[1]
            if u.state == problem.goalState:
                return solution(u)
            exp.add(u.state.toTuple())
            act = Problem.applicable(self,u.state)
            chil = []
            for k in act:
                child = child_node(u,k,p)
                ka = child.state.toTuple()
                if child not in exp:
                    child.f = child.cost + self.heuristic(child.state, p.goalState)
                    heapq.heappush(frontier,(child.f, child))
        return "Fake return value"

    # EXTRA CREDIT (OPTIONAL)
    def solve4x4(self, p: Problem) -> tuple:
        #reset the node counter for profiling
        #the serach should return the result of 'solution(node)'
        "*** YOUR CODE HERE ***"
        return "Fake return value"

if __name__ == '__main__':
    p=Problem()
    s=State()
    n=Node(None,None, 0, s)
    n2=Node(n,None, 0, s)

    searches = Searches()

    p.goalState=State(s)

    p.apply('R',s)
    p.apply('R',s)
    p.apply('D',s)
    p.apply('D',s)
    p.apply('L',s)

    p.initialState=State(s)

    print(p.initialState)

    si=State(s)
    # change the number of random moves appropriately
    # If you are curious see if you get a solution >30 moves. The 
    apply_rnd_moves(15,si,p)
    p.initialState=si

    startTime=time.perf_counter()


    print('\n\n=== BFS ===\n')
    startTime=time.perf_counter()
    res=searches.graph_bfs(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    print('\n\n=== Iterative Deepening DFS ===\n')
    startTime=time.perf_counter()
    res=searches.id_dfs(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    print('\n\n=== A*-Tree ===\n')
    startTime=time.perf_counter()
    res=searches.a_star_tree(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    print('\n\n=== A*-Graph ===\n')
    startTime=time.perf_counter()
    res=searches.a_star_graph(p)
    print(time.perf_counter()-startTime)
    print(Node.nodeCount)
    print(res)

    # EXTRA CREDIT (OPTIONAL)
    # UN-COMMENT the code below when you test this
    # change the 'boardSize' variable into 4 from slideproblem.py file
    """
    print('\n\n=== A*-solve4x4 ===\n')
    startTime = time.clock()
    res = searches.solve4x4(p)
    print(time.clock() - startTime)
    print(Node.nodeCount)
    print(res)
    """
