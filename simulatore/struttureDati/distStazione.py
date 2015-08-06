__author__ = 'maury'

import math as mt
import random as ran
import numpy as np
from itertools import count

class DistStazione():
    """
    Classe che identifica la distribuzione del tempo di servizio per ogni stazione
    Puo essere composta da piu distribuzioni
    """
    def __init__(self, staz, seme):
        self.id=staz.id
        self.tipo=staz.tipo
        self.distribuzioni = []
        for dist in staz.distr:
            self.distribuzioni.append(Distribuzione(dist,seme))
        if staz.tipo=="infinite":
            self.z=staz.z

    # Generazione di un tempo di servizio con distribuzione associata ad una stazione (self)
    def genDistr(self):
        if self.tipo=="server":
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
                    num+=((distr.info["b"]-distr.info["a"])*nCas+distr.info["a"])/1000
                elif distr.info["tipo"]=="normal":
                    giro=True
                    while giro:
                        listCas=distr.genSeqNum(12)
                        print "ARRAY:",listCas
                        normStand=np.sum(listCas)-6.0
                        norm=normStand*np.sqrt(distr.info["variance"])+distr.info["mean"]
                        if (norm>0)and(norm<30.0):
                            giro=False
                    num+=norm/1000
        # Caso in cui la stazione risulti essere una infinite server
        elif self.tipo=="infinite":
            num=self.z
        return num

    # Stampa delle diverse distribuzioni che formano il tempo di servizio di una stazione (self)
    def stampaDistr(self):
        print "\nLista di distribuzioni che formano il tempo di servizio della stazione:"
        print vars(self)
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

    def genNum(self):
        """
        Metodo che genera un numero casuale proseguedo lungo
        la sequenza di cui ci si era salvato lo stato
        :return: Numero casuale [0,1)
        """
        ran.setstate(self.stato)
        num=ran.random()
        self.setStato(ran.getstate())
        return num

    def genSeqNum(self,n):
        """
        Metodo che genera una Sequenza di numeri casuali proseguedo
        lungo la sequenza di cui ci si era salvato lo stato
        :param n: Numero di numeri casuali che si vogliono
        :return: Sequenza di numeri casuali [0,1)
        """
        listNum=[]
        ran.setstate(self.stato)
        for i in range(n):
            listNum.append(ran.random())
        self.setStato(ran.getstate())
        return np.array(listNum)

def genTempMisura(x):
    """
    Generazione della istanza dell'evento di misura in base al tempo di simulazione
    :param x: Tempo di simulazione
    :return: Istanza di tempo dell'evento di misura
    """
    return mt.pow(x,2)