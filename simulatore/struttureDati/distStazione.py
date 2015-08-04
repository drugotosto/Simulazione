__author__ = 'maury'

import random as ran
import numpy as np
from itertools import count

class DistStazione():
    """
    Classe che identifica la distribuzione del tempo di servizio per ogni stazione
    Puo essere composta da piu distribuzioni
    """
    def __init__(self, staz, seme):
        self.distribuzioni = []
        for dist in staz.distr:
            self.distribuzioni.append(Distribuzione(dist, seme))

    # Generazione di un tempo di servizio con distribuzione associata ad una stazione (self)
    def genDistr(self):
        num=0.0
        # Ciclo su tutte le distribuzioni che compongono la stazione di riferimento
        for distr in self.distribuzioni:
            if distr.info["tipo"]=="exponential":
                num+=-(np.log(distr.genNum())*distr.info["s"])
            elif distr.info["tipo"] == "erlang":
                listCas=distr.genSeqNum(distr.info['k'])
                print "ARRAY:",listCas
                num+=-((distr.info["s"]/distr.info['k'])*np.log(np.prod(listCas)))
            elif distr.info["tipo"]=="uniform":
                nCas=distr.genNum()
                num+=(distr.info["b"]-distr.info["a"])*nCas+distr.info["a"]
            elif distr.info["tipo"]=="normal":
                giro=True
                while giro:
                    listCas=distr.genSeqNum(12)
                    print "ARRAY:",listCas
                    normStand=np.sum(listCas)-6.0
                    norm=normStand*np.sqrt(distr.info["variance"])+distr.info["mean"]
                    if (norm>0)and(norm<30.0):
                        giro=False
                num+=norm
        return num

    # Stampa delle diverse distribuzioni che formano il tempo di servizio di una stazione (self)
    def stampaDistr(self):
        print "\nLista di distribuzioni che formano il tempo di servizio della stazione:"
        for distr in self.distribuzioni:
            print "Distribuzione:",distr.info

class Distribuzione():
    """
    Classe che identifica ogni singola distribuzione e che quindi oltre ai vari parametri
    che la identificano avra associata una determinata sequenza di istanze di variabili
    casuali uniformi e relativo stato del generatore che si andra ad aggiornare dopo ogni
    "pescata"
    """
    _seme = count(1)

    def __init__(self, dist, seme):
        self.info = dist

        if (seme == "debug"):
            ran.seed(self._seme.next())
        else:
            ran.seed()

        self.stato=ran.getstate()

    def setStato(self, stato):
        self.stato = stato

    def getStato(self):
        return self.stato

    # Metodo che genera un numero casuale proseguedo lungo la sequenza di cui ci si era salvato lo stato
    def genNum(self):
        ran.setstate(self.stato)
        num = ran.random()
        self.setStato(ran.getstate())
        return num

    # Metodo che genera una Sequenza di numeri casuali proseguedo lungo la sequenza di cui ci si era salvato lo stato
    def genSeqNum(self,n):
        listNum=[]
        ran.setstate(self.stato)
        for i in range(n):
            listNum.append(ran.random())
        self.setStato(ran.getstate())
        return np.array(listNum)
