__author__ = 'maury'
import itertools

def generaSpazioStati(n,m):
    comb=list(itertools.product(range(0,n+1), repeat=m))
    comb=[val for val in comb if sum(val)==n]
    return comb
