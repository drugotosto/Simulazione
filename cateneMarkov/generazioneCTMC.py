__author__ = 'maury'
import itertools

def generaCombinazioni():

    comb=list(itertools.product(range(0,4), repeat=3))
    print("COMBINAZIONI1:",comb)
    comb=[val for val in comb if sum(val)==3]
    return comb
