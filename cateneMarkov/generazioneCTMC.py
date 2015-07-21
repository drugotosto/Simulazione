__author__ = 'maury'
import itertools
from settaggi import m
from struttureDati.stato import Stato
from struttureDati.statoErlang import StatoErlang


# Generazione dello spazio degli stati valido anche in presenza di stazioni con distribuzione di Erlang
def generaSpazioStati(md,n):
    # Prodotto Cartesiano di tutti i possibili elementi dati dall'array (0,1,2,3,...15)
    comb = list(itertools.product(range(0, n + 1), repeat=m))
    # Si sottraggono poi tutti questi elementi la cui somma non arriva ad un totale di n
    comb = [val for val in comb if sum(val) == n]
    print "Spazio Originale:",comb,"\nlung:",len(comb)
    # Recupero lista degli indici stazioni che sono di tipo erlang_k
    ind_staz=[i for i,staz in enumerate(md.stazioni) if staz.tipo=="erlang"]
    spazio=[]
    # Ciclo su sutto lo spazio...
    for i,stat in enumerate(comb):
        statNorm=True
        posErl=[]
        # Ciclo tante volte quante sono le stazioni con distr. Erlang su uno stato specifico
        while len(ind_staz)>0:
            # Prelevo l'indice della stazione con distr. di Erlang
            ind=ind_staz.pop()
            # Controllo ogni posizione dello stato
            for j in range(len(md.stazioni)):
                # Controllo se lo stato risulta essere di Erlang o meno
                if (j==ind)and(stat[j]>0):
                    statNorm=False
                    posErl.append(j)
        mapStatPos=[stat,posErl]
        # Creazione oggetto classe "Stazione"
        if statNorm:
            spazio.append(Stato(stat))
        # Creazione oggetto classe "StazioneErlang"
        else:
            spazio.extend(creazioneStatiErlang(mapStatPos))

    return spazio

def creazioneStatiErlang(mapStatPos):
    spazio=[]
    return spazio

