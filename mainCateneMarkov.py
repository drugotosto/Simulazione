__author__ = 'maury'

"""
    MAIN PRINCIPALE
"""
import numpy as np
from settaggi import *
from cateneMarkov import *

if __name__=='__main__':
    print "Costruzione catena di Markov del modello dato come progetto finale (modello di un sistema)"

    spazio=generaSpazioStati(n,m)
    print "spazioINAZIONI:",spazio,"\nnumero:",len(spazio)

    # Dizionario con indice numerico 0,1,2,... con valori tuple formate da: ((x,x,x,x),'(x,x,x,x))
    vettPI={i:(stat,str(stat)) for i,stat in enumerate(spazio)}

    matQ=np.zeros((len(spazio),len(spazio)))
    print "Vettore:",vettPI