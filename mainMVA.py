__author__ = 'maury'

from settaggi import *
from analisiOperazionale import *
from struttureDati import gestoreModello as gsm
from mva import *

if __name__=='__main__':

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=gsm.caricamentoModello("parametri.json")
    # Calcolo le visite del modello prendendo come riferiemento la stazione 0(terminali collegati)
    calcoloVisite(md,indice_rif)

    # Calcolo delle varie domande alle varie stazioni
    domande=calcoloDomande(md)

    # Calcolo della somma delle domande (V*S) per le varie stazioni cioe = tempo di permanenenza con una sola persona dentro
    somDomande=0
    for val in domande:
        somDomande+=val

    dMax=max(controlloStazione(md))

    print "******IMPLEMENTAZIOME MVA ******"
    calcoloIndiciPrestazione(md)

    # Stampa dei grafici (settare opportunamente l'indice scelto)
    indici=gsm.ritornaIndice(md,'X')
    graficiIndice(indici)