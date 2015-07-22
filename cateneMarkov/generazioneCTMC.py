__author__ = 'maury'
import itertools
from settaggi import m
from struttureDati.stato import Stato,StatoErlang


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
        # Ciclo tante volte quante sono le stazioni con distr. Erlang su uno ogni specifico stato
        for ind in ind_staz:
            # Controllo ogni posizione dello stato
            for j in range(len(md.stazioni)):
                # Controllo se lo stato risulta essere di Erlang o meno
                if (j==ind)and(stat[j]>0):
                    statNorm=False
                    # Aggiorno la lista per definire su ogni stato quante/quali posizioni sono coinvolte
                    posErl.append(j)
        mapStatPos=[stat,posErl]
        # Creazione oggetto classe "Stazione"
        if statNorm:
            spazio.append(Stato(stat))
        # Creazione oggetto classe "StazioneErlang"
        else:
            """Funziona solo in presenza di al max 1 stazione ERLANG, con piu stazioni occorre
               rivedere la modalita di creazione degli stati per riuscire a considerare tutte
               le possibili combinazioni esistenti."""
            for val in mapStatPos[1]:
                for k in range(1,md.stazioni[val].k+1):
                    spazio.append(StatoErlang(mapStatPos[0],[val],[k]))
    return spazio

