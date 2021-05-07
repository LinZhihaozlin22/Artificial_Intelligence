"""
Probability models. (Chapter 13-15)
Nils Napp
Based on AIMA code
"""
import random
from numbers import Number

class ProbDist:
    """A discrete probability distribution. You name the random variable
    in the constructor, then assign and query probability of values.
    >>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; P['H']
    0.25
    >>> P = ProbDist('X', {'lo': 125, 'med': 375, 'hi': 500})
    >>> P['lo'], P['med'], P['hi']
    (0.125, 0.375, 0.5)
    """

    def __init__(self, varname='?', freqs=None, sample_space=None, vals=None):
        """If freqs is given, it is a dictionary of values - frequency pairs,
        then ProbDist is normalized."""
        self.prob = {}
        self.prob_vec =[] # Not yet used
        self.varname = varname
        self.values = []
        
        keys=()
        if freqs:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()
            self.sample_space=self.prob.keys()
            
        elif sample_space:
            assert isinstance(vals,(list,tuple)),  "'vals' must be a list or tuple of probabilities"
            assert isinstance(sample_space,(str,list,tuple)), "'sample_space must' be string or list"
            if isinstance(sample_space,str):
                sample_space=sample_space.split()
            assert isinstance(sample_space,(list,tuple))
            
            keys=sample_space
            
            assert len(keys)==len(vals), "Number of keys and values does not match"
            
            for k,p in zip(keys,vals):
                assert isinstance(p,Number), "Elements in vals must me numbers"
                self.prob[k]=p
            self.sample_space=sample_space
                
    def __getitem__(self, val):
        """Given a value, return P(value)."""
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        """Set P(val) = p."""
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0."""
        total = sum(self.prob.values())
        if not isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def show_approx(self, numfmt='{:.3g}'):
        """Show the probabilities rounded and sorted by key, for the
        sake of portable doctests."""
        return ', '.join([('{}: ' + numfmt).format(v, p)
                          for (v, p) in sorted(self.prob.items())])

    def __repr__(self):
        return "P({})".format(self.varname)

        
#---VVV---VVV---VVV------ Helper Functions 
        
def event_values(event, variables):
    """Return a tuple of the values of variables in event.
    >>> event_values ({'A': 10, 'B': 9, 'C': 8}, ['C', 'A'])
    (8, 10)
    >>> event_values ((1, 2), ['C', 'A'])
    (1, 2)
    """
    if isinstance(event, tuple) and len(event) == len(variables):
        return event #event is already a tuple
    else:
        return tuple([event[var] for var in variables])

        
def normalize(dist):
    """
    Multiply each number by a constant such that the sum is 1.0
    Can be applied to both dictionary distributions and lists/tuples
    """
    if isinstance(dist, dict):
        total = sum(dist.values())
        for key in dist:
            dist[key] = dist[key] / total
            assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
        return dist
    total = sum(dist)
    return [(n / total) for n in dist]

try:  # math.isclose was added in Python 3.5; but we might be in 3.4
    from math import isclose
except ImportError:
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        """Return true if numbers a and b are close to each other."""
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

#------------------

class BayesNet:
    """Bayesian network"""
    
    def __init__(self, node_specs=[]):
        """Nodes must be ordered with parents before children."""
        self.nodes = []
        self.variables = []
        for node_spec in node_specs:
            self.add(node_spec)

    def add(self, node_spec):
        """Add a node to the net. Its parents must already be in the
        net, and its variable must not."""
        node = BayesNode(*node_spec)
        assert node.variable not in self.variables
        assert all((parent in self.variables) for parent in node.parents)
        self.nodes.append(node)
        self.variables.append(node.variable)
        for parent in node.parents:
            parent_node=self.variable_node(parent)
            parent_node.child_nodes.append(node)
            node.parent_nodes.append(parent_node)
            
    def variable_node(self, var):
        """Return the node for the variable named var."""
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("No such variable: {}".format(var))

    def variable_values(self, var):
        """Return the domain of var."""
        n=self.variable_node(var)
        return n.sample_space
                
    def _check_names(self):
        """Check that the parent domain names and the cpt tuples in the children match"""
        pass
    
    def _check_cpt_keys(self,var):
        
        pass   
        
    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)

class BayesNode:
    """A conditional probability distribution, P(X | parents). Part of a BayesNet."""

    def __init__(self, X :str, sample_space, parents, cpt :dict):
        """
        * 'X' is the variable name
        
        * 'sample_space' is a list/tuple, or space deliminated string of possile values.
           The values cannot themselves be tuples.
           Speical case: empty string or None will be treated as (True,False)
 
        * 'parents' is a list/tuple or space deliminate string of parent  names
        
        * 'cpt' is a dictionary where the variable assigments of the parens are
           a tuple i.t.  {(v1, v2, ...): (p1, p2, p3 ...), ...}, the distribution 
           P(X | parent1=v1, parent2=v2, ...) = p. Each key must have as many
          values as there are parents. Each probability distribution must have 
          as many elements as there are in 'sample_space'
                    
        * 'cpt' can be given as {v: (p1, p2, p3, ..),  ...}, the conditional 
          probability distribution P(X| parent=v). When there's just one parent, i.e.
          the tuple parentases can be dropped for single item key
       
        Examples:    
        
        Base node, no parents, with a sample space of three outomces called valN     
        >> BayesNode('BaseRV','val1 val2 val3','',(0.1, 0.8, 0.1))
        
        Base node using a default binary RV
        >> BayesNode('BaseRV',(True,False),'',(0.1, 0.8)) 
        >> BayesNode('BaseRV','','',(0.1, 0.8)) 
     
        One Parent binary RV with a binary parent
        >> BayesNode('OneParentRV','','MyParent',{True:(0.2,0.8), False:(0.8,0.2)})
        
        One Parent RV with a binary parent
        >> BayesNode('OneParentRV','val1 val2 val3','MyParent',{True:(0.2,0.7,0.1), False:(0.8,0.1,0.1)})

        One Parent RV with a parent sample space ('val1',val2','val3')
        >> BayesNode('OneParentRV','val1 val2 val3','MyParent',{'val1':(0.2,0.7,0.1),
                                                                'val2':(0.8,0.1,0.1)
                                                                'val3':(0.8,0.1,0.1)})

        Two parent RV with a parent sample spaces ('val1',val2','val3')
        >> BayesNode('OneParentRV','val1 val2 val3','p1 p2',{('val1', 'val1'):(0.2,0.7,0.1),
                                                                ('val1', 'val2'):(0.8,0.1,0.1)
                                                                ('val1', 'val3'):(0.8,0.1,0.1)
                                                                ...
                                                                ('val3', 'val3'):(0.8,0.1,0.1)
                                                                })
        """
                             
        # Check and create the sample space
        if sample_space=='' or sample_space==None:
            sample_space=(True,False)
        
        if isinstance(sample_space,str):
            sample_space=sample_space.split()
            
        assert isinstance(sample_space,(list,tuple)), "'sample_space' has wrong type"

        # Check the parents
        if isinstance(parents, str):
            parents = parents.split()

        """
        Parse and setup the cpt
        first convert into tuple keys
        then check and normalize the distributions
        """
        if isinstance(cpt, (list, tuple)):  # no parents, 0-tuple
            assert len(parents)==0, 'Can only use tuple notation for root nodes'
            cpt = {(): cpt}

        elif isinstance(cpt, dict):
            # one parent, 1-tuple            
            if cpt and not isinstance(list(cpt.keys())[0], tuple):
                assert len(parents)==1, 'Can only use non-tuple keys for one-parent nodes'
                cptNew={}    
                for v,p in cpt.items():
                    assert isinstance(p,(list,tuple)) and len(sample_space)==len(p) , 'distribution of wrong length or type'
                    cptNew[(v,)]=p
                cpt=cptNew

                    
        assert isinstance(cpt, dict)
        #check prob dist and types for dict if it was passed through
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert isinstance(p,(list,tuple)) and len(sample_space)==len(p)
            assert all(0 <= pv <= 1 for pv in p), 'vector entires pi must be 0<=pi<=1'
            assert sum(p) <= 1 or sum(p) >= 0.98, 'Probability must sum to 1: ' + str(p) + '->' + str(sum(p))  
            cpt[vs]=p

        """
        dictionary for looking up the index of samples in the distribuiton  
        """
        idx=dict(zip(sample_space,range(len(sample_space))))

        """
        assign the node properies
        """
        self.variable = X
        self.parents = parents
        self.sample_space= tuple(sample_space)
        self.idx=idx
        self.cpt = cpt
        self.child_nodes = []
        self.parent_nodes=[]

    def p(self, value, evidence):
        """Return the conditional probability
        P(X=value | parents=parent_values), where parent_values
        are the values of parents in evidence. (evidence must assign each
        parent a value, but could include more variables)
        """
        assert value in self.sample_space, "'value' is not in sample space"                
        return  self.cpt[event_values(evidence, self.parents)][self.idx[value]]

    def sample(self, event):
        """Sample from the distribution for this variable conditioned
        on event's values for parent_variables. 
        """
        
        '''
        In Python 3.6 and up you can use random.choices
        Here we do the lookup using the uniform random number generator

        If you do a lot of sampling, then the cumulative sums should 
        be pre-copmtued and stored during initialization
        '''

        r=random.random()
        acc=0
        i=0
        
        for p in self.cpt[event_values(event, self.parents)]:
            acc += p
            if r <= acc:
                break
            i += 1
            
        assert i<len(self.sample_space), "random index is out of bounds. Make sure conditional probability talbe sumsto 1"
            
        return self.sample_space[i]

    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))