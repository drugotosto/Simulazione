__author__ = 'maury'

import random as ran
from itertools import count

class DistStazione():
    def __init__(self,staz,seme):
        self.id=staz.id
        self.tipo=staz.tipo
        self.distribuzioni=[]
        for dist in staz.distr:
            self.distribuzioni.append(Distribuzione(dist,seme))


class Distribuzione():
    def __init__(self,dist,seme):
        self.info=dist
        self.sequenze=[]
        """
           A seconda della tipologia di distribuzione avro bisogno
           di un numero diverso di sequenze di numeri casuali da
           cui continuero ad estrarre numeri per generarle
        """
        if dist.tipo=="exponential":
            self.sequenze.append(Sequenza(seme))
        if dist.tipo=="erlang":
            pass
        if dist.tipo=="uniform":
            self.sequenze.append(Sequenza())
        if dist.tipo=="normal":
            for i in range(12):
                self.sequenze.append(Sequenza())


class Sequenza():
    _seme=count(1)
    def __init__(self,seme):
        if(seme==1):
            self.seed=self._seme.next()
        else:
            self.seed=seme
        ran.seed(self.seed)
        self.stato=ran.getstate()

    def setStato(self,stato):
        self.stato=stato