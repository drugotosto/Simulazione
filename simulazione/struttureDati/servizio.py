from __builtin__ import dict

__author__ = 'maury'

import math as mt
import random as ran
import numpy as np
import pyprimes as pr
from settaggiSim import debug, maxRange
from itertools import count

contatotore=count(5)

class Servizio():
    """
    Classe che identifica le (possibili) diverse distribuzioni del tempo di servizio di ogni stazione
    """
    def __init__(self,staz):
        """
        Costruttore del tempo di servizio della stazione
        :param gen: Istanza di un generatore di numeri casuali per ogni stazione (server) e
        tra di loro non condividono lo stato.
        Istanzio un generatore di numeri casuali (condiviso dalle diverse v.c. che formano
        il tempo di servizio della stazione 'server') utilizzato per generare istanze delle
        diverse distribuzioni.
        """
        self.gen=ran.Random()
        self.distribuzioni = []
        if staz["tipo"]=="infinite":
            self.distribuzioni.append(Distribuzione(self.gen))
            self.z=staz["z"]
        else:
            for distr in staz["distr"]:
                self.distribuzioni.append(Distribuzione(self.gen,distr=distr))

    def genDistrIF(self):
        # print "\nEstraggo exp di media:",self.z
        num=(-np.log(self.distribuzioni[0].genNum()))*self.z
        return num

    # Generazione di un tempo di servizio con distribuzione associata ad una stazione (self)
    def genDistr(self):
        num=np.float(0)
        # Ciclo su tutte le distribuzioni che compongono la stazione di riferimento
        for distr in self.distribuzioni:
            if distr.tipo=="exponential":
                # print "\nEstraggo exp di parametro:",(1.0/distr.s)
                num+=(-np.log(distr.genNum()))*distr.s
            elif distr.tipo=="erlang":
                print "\nEstraggo ERLANG di parametro:",distr.s,"k=",distr.k
                listCas=distr.genSeqNum(distr.k)
                print "Sequenza num. casuali:",listCas
                num+=(-np.log(np.prod(listCas)))*(distr.s/distr.k)
            elif distr.tipo=="uniform":
                nCas=distr.genNum()
                num+=((distr.b-distr.a)*nCas+distr.a)/1000
            elif distr.tipo=="normal":
                giro=True
                norm=0.0
                while giro:
                    listCas=distr.genSeqNum(12)
                    normStand=np.sum(listCas)-6.0
                    norm=normStand*np.sqrt(distr.variance)+distr.mean
                    if (norm>0)and(norm<30.0):
                        giro=False
                num+=norm/1000
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
    casuali uniformi (per via di aver inizializzato il generatore con semi diversi)
    e relativo stato del generatore che si andra ad aggiornare dopo ogni "pescata"
    """

    def __init__(self,gen,distr=None):
        if distr!=None:
            # La Distribuzione NON appartiene ad un I.S.
            self.__dict__.update(distr)
        self.gen=gen
        # Inizializza per ogni distribuzione il generatore con un seme diverso
        self.gen.seed(generaSeme())
        # Rappresenta lo stato interno corrente del generatore utilizzato poi per estrarre il successivo num. casuale
        self.stato=self.gen.getstate()

    def genNum(self):
        """
        Metodo che genera un numero casuale proseguedo lungo
        la sequenza di cui ci si era salvato lo stato
        :return: Numero casuale [0,1)
        """
        self.gen.setstate(self.stato)
        num=self.gen.random()
        self.stato=self.gen.getstate()
        return num

    def genSeqNum(self,n):
        """
        Metodo che genera una Sequenza di numeri casuali proseguedo
        lungo la sequenza di cui ci si era salvato lo stato
        :param n: Numero di numeri casuali che si vogliono
        :return: Sequenza di numeri casuali [0,1)
        """
        listNum=[]
        self.gen.setstate(self.stato)
        for i in range(n):
            listNum.append(self.gen.random())
        self.stato=self.gen.getstate()
        return listNum

def generaSeme():
    if debug:
        # Produce il successivo numero primo in ordine
        num=pr.nth_prime(contatotore.next())
    else:
        # Produce il successivo numero primo scelto a caso
        num=pr.nth_prime(ran.randint(0,maxRange))
    # print "NUM PRIMO scelto per il seme:",num
    return num


def genTempMisura(x):
    """
    Generazione della istanza dell'evento di misura in base al tempo di simulazione
    :param x: Tempo di simulazione
    :return: Istanza di tempo dell'evento di misura
    """
    if x<256:
        return mt.pow(x,2)
    else:
        return x*2


