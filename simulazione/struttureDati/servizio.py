from __builtin__ import dict

__author__ = 'maury'

import math as mt
import random as ran
import numpy as np
from itertools import count

class Servizio():
    """
    Classe che identifica le (possibili) diverse distribuzioni del tempo di servizio di ogni stazione
    """
    def __init__(self,staz,debug):
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
        for distr in staz["distr"]:
            self.distribuzioni.append(Distribuzione(distr,debug,self.gen))


    # Generazione   di un tempo di servizio con distribuzione associata ad una stazione (self)
    def genDistr(self):
        num=np.float(0)
        # Ciclo su tutte le distribuzioni che compongono la stazione di riferimento
        for distr in self.distribuzioni:
            if distr.tipo=="exponential":
                print "\nEstraggo exp di parametro:",(1.0/distr.s)
                num+=-(np.log(distr.genNum())/(1.0/distr.s))
            elif distr.tipo == "erlang":
                print "DISTR:",distr.info
                # print "\nEstraggo ERLANG di parametro:",distr["s"],"k=",distr["k"]
                listCas=distr.genSeqNum(distr.k)
                print "ARRAY:",listCas
                num+=-((distr.info["s"]/distr.k)*np.log(np.prod(listCas)))
            elif distr.tipo=="uniform":
                nCas=distr.genNum()
                num+=((distr.b-distr.a)*nCas+distr.a)/1000
            elif distr.tipo=="normal":
                giro=True
                norm=0.0
                while giro:
                    listCas=distr.genSeqNum(12)
                    print "ARRAY:",listCas
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
    _seme = count(1)

    def __init__(self,dist,debug,gen):
        # self.info=dist
        self.__dict__.update(dist)
        self.gen=gen
        if debug:
            # Inizializzo l'istanza del generatore di num. casuali utilizzando un valore fisso come debug inziale
            self.gen.seed(self._seme.next())
        else:
            # Inizializzo istanza di generatore di num. casuali utilizzando il tempo corrente come debug inziale
            self.gen.seed()
            # Rappresenta lo stato interno corrente del generatore utilizzato poi da "setstate()"
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
        return np.array(listNum)

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

class Servizio2():
    """
    Classe che identifica le (possibili) diverse distribuzioni del tempo di servizio di ogni stazione
    """
    def __init__(self,staz,debug):
        """
        Costruttore del tempo di servizio della stazione
        :param gen: Istanza di un generatore di numeri casuali per ogni stazione (server) e
        tra di loro non condividono lo stato.
        Istanzio un generatore di numeri casuali (condiviso dalle diverse v.c. che formano
        il tempo di servizio della stazione 'server') utilizzato per generare istanze delle
        diverse distribuzioni.
        """
        self.distribuzioni = []
        for distr in staz["distr"]:
            self.distribuzioni.append(Distribuzione2(distr,debug))


    # Generazione   di un tempo di servizio con distribuzione associata ad una stazione (self)
    def genDistr(self):
        num=np.float(0)
        # Ciclo su tutte le distribuzioni che compongono la stazione di riferimento
        for distr in self.distribuzioni:
            if distr.tipo=="exponential":
                print "\nEstraggo exp di parametro:",(1.0/distr.s)
                num+=-(np.log(distr.genNum())/(1.0/distr.s))
            elif distr.tipo == "erlang":
                print "DISTR:",distr.info
                # print "\nEstraggo ERLANG di parametro:",distr["s"],"k=",distr["k"]
                listCas=distr.genSeqNum(distr.k)
                print "ARRAY:",listCas
                num+=-((distr.info["s"]/distr.k)*np.log(np.prod(listCas)))
            elif distr.tipo=="uniform":
                nCas=distr.genNum()
                num+=((distr.b-distr.a)*nCas+distr.a)/1000
            elif distr.tipo=="normal":
                giro=True
                norm=0.0
                while giro:
                    listCas=distr.genSeqNum(12)
                    print "ARRAY:",listCas
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

class Distribuzione2():
    """
    Classe che identifica ogni singola distribuzione e che quindi oltre ai vari parametri
    che la identificano avra associata una determinata sequenza di istanze di variabili
    casuali uniformi (per via di aver inizializzato il generatore con semi diversi)
    e relativo stato del generatore che si andra ad aggiornare dopo ogni "pescata"
    """
    _seme = count(1)

    def __init__(self,dist,debug):
        # self.info=dist
        self.__dict__.update(dist)
        self.gen=ran.Random()
        if debug:
            # Inizializzo l'istanza del generatore di num. casuali utilizzando un valore fisso come debug inziale
            self.gen.seed(self._seme.next())
        else:
            # Inizializzo istanza di generatore di num. casuali utilizzando il tempo corrente come debug inziale
            self.gen.seed()
            # Rappresenta lo stato interno corrente del generatore utilizzato poi da "setstate()"

    def genNum(self):
        """
        Metodo che genera un numero casuale proseguedo lungo
        la sequenza di cui ci si era salvato lo stato
        :return: Numero casuale [0,1)
        """
        num=self.gen.random()
        return num

    def genSeqNum(self,n):
        """
        Metodo che genera una Sequenza di numeri casuali proseguedo
        lungo la sequenza di cui ci si era salvato lo stato
        :param n: Numero di numeri casuali che si vogliono
        :return: Sequenza di numeri casuali [0,1)
        """
        listNum=[]
        for i in range(n):
            listNum.append(self.gen.random())
        return np.array(listNum)