'''
Structure written by: Nils Napp
Modified & Solution by: Jiwon Choi (F18 HW script)
'''
from bayesnets import (ProbDist, BayesNode, BayesNet)
import random

class Inference:
    '''
    Class to generate inference algorithms on Bayesian Networks
    * 1. Enumeraiton (produce all the terms in the joing and then marginalize)
    * 2. Rejection Sampling
    * 3. Likeliehood Weighting
    '''
    def __init__(self, bayesian_network, evidence = {}):
        self.net=bayesian_network
        self.evidence=evidence

    def sample(self) -> dict:
        """ Return sample from network:
        Sample should be a dictionary where the keyes are
        variable names and elemnts of their sample sapce
        """
        samp = {}
        for node in self.net.nodes:
            samp[node.variable] = node.sample(samp)
        return samp

    def copy_assign(self,ev,X,xval):
        '''
        return a copy of the evidence dictionary with X:xval appended
        this is useful for recursive enumerations of all assignments since
        otherwise changing the dictionary would have side effects outside
        the call, though it is entierly optional
        '''
        e=ev.copy()
        e[X]=xval
        return e

    def enumeration_infer(self, X, e=None) -> ProbDist:
        """
        TODO: Return the conditional probability distribution of variable X
        given evidence e
        """

        # Use evidence passed to function call, otherwise use default
        if e==None:
             e=self.evidence

        assert X not in e, 'Query variable must be distinct from evidence'
        assert X in self.net.variables, 'Variable needs to be in network'

        """
        * Initialize a probability distribution
        * For each outcome sum over all the hidden variables
        * Normalize
        """

        """YOUR CODE"""
        q = ProbDist(X)
        value = self.net.variable_values(X)
        for i in value:
            q[i] = self.enu_all((self.net.variables),self.copy_assign(e,X,i))
        return q.normalize() # <- may need to tweak a bit

    def enu_all(self,var,e):
        if len(var) == 0:
            return 1
        Y = var[0]
        if Y in e:
            return (self.net.variable_node(Y).p(e[Y],e)) * (self.enu_all(var[1:],e))
        else:
            y = self.net.variable_values(Y)
            su = 0
            for o in y:
                su += self.net.variable_node(Y).p(o,e) * (self.enu_all(var[1:],self.copy_assign(e,Y,o)))
            return su
        

    def rejection_sampling(self,X :str, N :int, e :dict = None) -> ProbDist:
        """
        TODO: Estimate the probability distribution of variable X given using
        N samples and evidence e. If not evidence is given, use the default
        for the Inference object.
        """
        if e==None:
            e=self.evidence

        vec = dict((x, 0) for x in diagnoseNet.variable_values(X))
        """YOUR CODE"""
        for j in range(N):
            sample = self.sample()
            if all(item in sample.items() for item in e.items()):
                vec[sample[X]] += 1
        return ProbDist(X,vec) # <- put parameters in it

    def likelihood_weighting(self, X :str, N:int, e : dict =None) -> ProbDist:
        """
        TODO: Estimate the probability distribution of variable X given evidence e.
        """
        if e==None:
            e=self.evidence

        W = dict((x, 0) for x in diagnoseNet.variable_values(X))
        for j in range(N):
            x,w = self.weighted_sample(e)
            W[x[X]] += w
        return ProbDist(X,W) # <- put parameters in it

    def weighted_sample(self,e :dict = None) -> (dict,float):
        """
        TODO: Sample an event from bn that's consistent with the evidence e;
        return the event and its weight, the likelihood that the event
        accords to the evidence.
        """

        """YOUR CODE"""
        w = 1
        x = e.copy()

        for node in diagnoseNet.nodes:
            """
            P = {}
            for p in node.parents:
                P[p] = e.get(p) """
            Xi = node.variable
            if Xi in e:
                w *= node.p(e[Xi],x)
            else:
                x[Xi] = node.sample(x)

        return x,w# <- fake value, only type of variables are same

diagnoseNet=BayesNet([('Healthy','','',(0.8,0.2)),
                      ('FluShot','','',(0.6,0.4)),
                      ('Flu','','Healthy FluShot',{(True,True):(0,1.0),
                                                   (True,False):(0,1.0),
                                                   (False,True):(0.1,0.9),
                                                   (False,False):(0.4,0.6)}),
                      ('Lyme','', 'Healthy',{True: (0,1.0)  , False:(0.01,0.99)}),
                      ('Numbness','','Lyme',{True: (0.8,0.2), False:(0.3,0.7)}),
                      ('Fever','','Flu',{True:(0.9,0.1), False:(0.2,0.8)}),
                      ('Vomit','','Flu',{True:(0.8,0.2), False:(0.1,0.9)}),
                      ('Fatigue','','Lyme Flu',{(True,True):(0.99,0.01),
                                                (True,False):(0.8,0.2),
                                                (False,True):(0.9,0.1),
                                                (False,False):(0.4 , 0.6)})])

'''Please Build the Bayes net from the provided diagram'''
awakeNet=awakeNet = BayesNet([('T','<6 <7 <8 <9 >9', '', (0.3, 0.1, 0.1, 0.1, 0.4)),
                     ('A','', 'T', {'<6':(0.05,0.95),
                                     '<7':(0.3,0.7),
                                     '<8':(0.8,0.2),
                                     '<9':(0.9,0.1),
                                     '>9':(0.95,0.05)}),
                     ('L','','A', {True:(0.7,0.3),
                                   False:(0.2,0.8)}),
                     ('N','quiet snore blanket steps','A', {True:(0.2,0.01,0.29,0.5),
                                   False:(0.6,0.29,0.1,0.01)})])# <-------- Your declaration goes here
                      # <-------- Your declaration goes here

if __name__ == '__main__':
    '''
    Example Uses of ProbDist:
        There are two ways to initialize distributions
        * Give it dictionary where the keys are the element of the sample space
          and the values are counte or un-normalized probablities <<-- Will use this one
        * Give a sample_space list/tuple of domain values and a list/tuple that defines
          the distibution
    '''

    ''' roll virtual dice '''
    counts={}
    for i in range(1,6+1):
        counts[i]=0
    for rolls in range(100):
        roll=round((random.random()*6 -0.5))+1 #scale and shift so round will work
        counts[roll] +=1
    print('Raw counts: ' + str(counts))
    pdice=ProbDist('Dice',counts)
    print('ProbDist Object: ' + str(pdice))
    print('Probability Dsitribution: ' + str(pdice.show_approx()))

    '''
    BayesNodes and BayesNets
    Each node is specified with its parent names and the neccesarey CPT
    The CPTs are a little tricky. They are a dictionary where the keys are tuples
    of possible values from the sample space of the parent domains. The value
    is a probability vector that has the same length as the sample space.
    '''

    testNode=BayesNode('Node','val1 val2 val3',
                       'A/B-Parent C/D-Parent',
                       {('A','C'):(0.1, 0.2, 0.7),
                        ('A','D'):(0.3, 0.5, 0.2),
                        ('B','C'):(0.0, 0.2, 0.8),
                        ('B','D'):(0.998, 0.001, 0.001)})

    '''
    * The tuple order is the same as the order listed in the parents string
    * Both the sample space and the partents can be given a lists/tuples
    * If sample space is '' or None then the samples space defaults to (True,False)
    * When there are no parents, the CPT can jsut be given as a vector of appropriate lenght
    '''

    '''
    Working with these Bayes nets, events and samples are given as dictionaries
    To sample from a node you need an event (aka specific assignment) that specifies
    the parents, but the event could include more values.
    '''
    evidence={'A/B-Parent':'A', 'C/D-Parent':'C','SomeT/F-parent':True}

    '''Return the probability of a specific value given the evidence'''
    testNode.p('val2',evidence)

    '''
    Sample from the distribution given evidence. The values will be
    drawn from the sample_space according to the probability vector
    '''

    for i in range(10):
        print("Sampling given 'A/B-Parent'='A'" + " and 'C/D-Parent'='C' --> "
              + testNode.sample(evidence) )

    '''
    A BayesNet is made up of a bunch of nodes.
    During the specificaion they need to be added in such an order that the
    parents always preceed their children. This makes sampling and
    manipulation _MUCH_ easier. When you iterate  along the list of varialbes
    to pick events, then the later ones will have their parents picked so you
    can use both node.p(val,e) and node.sample(e) as long as e has the previous
    nodes in it. In the example below, the parents can come in either order, but must
    be added beofre 'Node'. The 'T/F-Node' must be last:

                  A/B-Parent   C/D-Parent
                        \       /
                         \     /
                          V   V
                           Node -------> T/F-Node

    '''

    abcdNet=BayesNet([('A/B-Parent','A B','',(0.1, 0.9)),
                      ('C/D-Parent','C D','',(0.7, .3)),
                      ('Node','val1 val2 val3',
                       'A/B-Parent C/D-Parent',
                       {('A','C'):(0.1, 0.2, 0.7),
                        ('A','D'):(0.3, 0.5, 0.2),
                        ('B','C'):(0.0, 0.2, 0.8),
                        ('B','D'):(0.998, 0.001, 0.001)}),
                       ('T/F-Node','','Node',{'val1':(0.1, 0.9),
                                              'val2':(0.6, 0.4),
                                              'val3':(0.4, 0.6)})
                      ])

    '''
    The 'T/F-Node' uses some shortcuts:
    * The '' for sample_space means (True,False)
    * When there is only a single parent, you can drop the tuple notation
    in the keys for the CPT
    '''

    '''
    Example Usage of the InferenceClass
    '''
    inferHealth=Inference(diagnoseNet)

    #used in rejection sampling
    randomEvent=inferHealth.sample()
    print('\n\nRandom Sample from Net' + str(randomEvent))

    #set evidence for inference problem and then try a few methods
    '''
    These should not work/do mutch until until you implement them!!
    However, there are some test cases with the restulst given the comments
    '''

    ev={'FluShot':False, 'Fatigue':True, 'Healthy':False, 'Flu':False}
    inferHealth.evidence=ev
    plymeW=inferHealth.likelihood_weighting('Lyme',1000)
    plymeR=inferHealth.rejection_sampling('Lyme',1000)
    plymeExact=inferHealth.enumeration_infer('Lyme')

    print("\n\nCompare Inference Techniques")
    print(plymeW.show_approx())     #<-- False ~ .98
    print(plymeR.show_approx())     #<-- False ~ .98 but can evaluate to  (1,0) due to sampling error
    print(plymeExact.show_approx()) #>>False: 0.98, True: 0.0198

    plymeExact=inferHealth.enumeration_ask('Lyme',{})
    print(plymeExact.show_approx())
    #Lyme disease 0.2% given nothing

    ev={'FluShot':True, 'Fatigue':True}
    plymeExact=inferHealth.enumeration_ask('Lyme',ev)
    print(plymeExact.show_approx())
    #Lyme disease 0.399% given fluShot & fatigue
