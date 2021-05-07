# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 11:03:51 2017
@author: Nils Napp

Modified on Thu Sep 5 21:35:17 2019
@modified by: Jiwon Choi
"""

import numbers
import random

class State:
    """ State of sliding number puzzle
        Contains array of values called 'board' to indicate
        tile positions, and the position of tile '0', which
        indicates the empty space on the board.         """
    
    boardSize=3

    def __init__(self,s=None):

        if s == None:
            
            tiles=range(self.boardSize*self.boardSize).__iter__()
            self.board=[[next(tiles) for i in range(self.boardSize)] for j in range(self.boardSize)]

            #keep track of empty position
            self.position=[0,0]
        
        else:
            
            #copy the board

            self.board=[]
            for row in s.board:
                self.board.append(list(row))

            #copy the positions    
            self.position=list(s.position)
            
        
    def __str__(self):
        #won't work for larger boards 
        rstr=''
        for row in self.board:
            rstr += str(row) + '\n'
        return rstr
    
    #overload to allow comparison of lists and states with ==
    def __eq__(self,other):
        if isinstance(other, State):
            return self.board == other.board
        elif isinstance(other,list):
            return self.board == other
        else:
            return NotImplemented
 
    def __lt__(self,other):
        if isinstance(other, State):
            return self.h < other.h
        else:
            return NotImplemented

    #turn into immutable ojbect for set lookup
    def toTuple(self):
        tpl=()
        for row in self.board:
            tpl += (tuple(row),)
        return tpl
    
    #create board from a list or tuple 
    def setBoard(self,brd):
        self.board=brd
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.board[row][col]==0:
                    self.position=[row,col]
                    return None
        assert False, 'Set board configuration does not have an empy spot!'

#node class for serach graph        
class Node:
    
    nodeCount=0
    
    def __init__(self,parent=None, action=None, cost=0, state=None):
        
        #keep track of how many nodes were created
        self.__class__.nodeCount += 1    
        self.nodeID=self.nodeCount
        
        self.parent=parent
        self.cost=cost
        self.action=action
        self.state=state
        self.f=0
        
    #test equivalence Should be state

    def __str__(self):
        rstr= 'NodeID: ' + str(self.nodeID) + '\n'
        if self.parent != None:
            rstr+='Parent: ' + str(self.parent.nodeID) + '\n'
        if self.action != None:
            rstr+='Action: ' + self.action  + '\n'
        rstr+='Cost:   ' + str(self.cost) + '\n'
        rstr+='State:\n' + str(self.state)
        return rstr
            
    def __lt__(self,other):
        if isinstance(other,Node):
            return self.f < other.f
        if issubclass(type(other),numbers.Real):
            return self.f < other
        else:
            return NotImplemented 

            
        
#problem
class Problem:
    """Class that defines a serach problem"""

    def __init__(self):
        self.actions=['U','L','D','R']
        self.initialState=0
        self.goalState=0

    def apply(self,a,s):

        #positions after move, still refers to s.position object
        post=s.position

        #make a copy
        pre=list(post)
        
        #compute post position
        if a == 'U':
            post[0]=max(pre[0]-1,0)
        elif a == 'L':            
            post[1]=max(pre[1]-1,0)
        elif a == 'D':
            post[0]=min(pre[0]+1,s.boardSize-1)
        elif a == 'R':
            post[1]=min(pre[1]+1,s.boardSize-1)
        else:
            print('Undefined action: ' + str(a))
            assert False, 'Action not defined for this problem!'

        #store the old tile
        tile=s.board[pre[0]][pre[1]]
        
        s.board[pre[0]][pre[1]]=s.board[post[0]][post[1]]
        s.board[post[0]][post[1]]=tile      

 #       print pre, ' ', post,' ',s.board[pre[0]][pre[1]] , '<--', s.board[post[0]][post[1]]      

        return s
        
    def applicable(self,s):
        actionList=[]

        #check if actions are applicable
        #Not in top row
        if s.position[0]>0:
            actionList.append('U')

        #not in left most col
        if s.position[1]>0:
            actionList.append('L')

        #not in bottom row
        if s.position[0]<(s.boardSize-1):
            actionList.append('D')

        #not in right col
        if s.position[1]<(s.boardSize-1):
            actionList.append('R')

        return actionList

    def goalTest(self,s):
        return self.goalState==s    


        
def child_node(n , action, problem):
    return Node(n,action, n.cost + 1, problem.apply(action,State(n.state)))

        
def apply_rnd_moves(numMoves,s,p):
    for i in range(numMoves):
        p.apply(p.actions[random.randint(0,3)],s)
    
def solution(node):
    ''' Returns actionList, cost of the solution generated from the node'''

    actions=[]
    cost=node.cost

    while node.parent != None:
        actions.insert(0,node.action)
        node=node.parent    

    return actions, cost        
