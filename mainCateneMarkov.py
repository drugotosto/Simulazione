__author__ = 'maury'

"""
    MAIN PRINCIPALE
"""
import numpy as np
from settaggi import *
from cateneMarkov import *
from struttureDati import gestoreModello as gsm

if __name__=='__main__':
    print "Costruzione catena di Markov del modello dato come progetto finale (modello di un sistema)"

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=gsm.caricamentoModello("parametri.json")

    spazio=generaSpazioStati(n,m)
    print "spazio:",spazio,"\nnumero:",len(spazio)

    # Dizionario con indice numerico 0,1,2,... con valori tuple formate da: ((n,n,n,n),'(n,n,n,n),'xi')
    spazioStati={i:(stat,str(stat),'x'+str(i)) for i,stat in enumerate(spazio)}

    gsm.aggiungiSpazio(md,spazioStati,n)

    matQ=np.zeros((len(spazio),len(spazio)))
    print "Spazio deglis stati:",spazioStati


