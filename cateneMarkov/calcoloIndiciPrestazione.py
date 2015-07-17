__author__ = 'maury'
from settaggi import m

# Settaggio delle varie P(k,n) per le diverse stazioni dato la distr. di prob. per un dato valore di n
def settaggioProbStaz(md,piG,n):

    # lista di prob per ogni stazione di dimensione N
    listaP=np.zeros(n)

    for i,p in enumerate(piG):
        print "Valore di prob:",piG,"corrispondente allo stato:",md.spazioStati[i][0]




