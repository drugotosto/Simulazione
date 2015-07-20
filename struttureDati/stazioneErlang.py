__author__ = 'maury'
from struttureDati import stazione

"""
    Classe che mi rappresenta le stazioni di tipo Erlang_k (sottoclasse della classe Stazione)
    - k
"""

import numpy as np

class StazioneErlang():
    def __init__(self,stazione,n):
        # self.__dict__.update(stazione)
        self.id=stazione["id"]
        self.nome=stazione["nome"]
        self.tipo=stazione["tipo"]
        self.s=np.float64(stazione["s"])
        self.visite=np.float64(0)
        self.domande=np.float64(0)
        self.indici={'X':np.zeros(n),'W':np.zeros(n),'N':np.zeros(n),'U':np.zeros(n),'R':np.zeros(n)}
        self.prob=dict.fromkeys(range(n+1),np.float64(0))
        self.indiciMark={'X':np.zeros(n),'W':np.zeros(n),'N':np.zeros(n),'U':np.zeros(n),'R':np.zeros(n)}
        self.k=stazione["k"]


