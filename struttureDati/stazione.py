__author__ = 'maury'

"""
    Classe che mi rappresenta la singola stazione con attributi recuperati dal file json + calcolati
    - id
    - nome
    - s
    - tipo
    - visite
    - domande
    - indici di prestazione (X,W,N,U)
"""

import numpy as np

class Stazione():
    def __init__(self,stazione,dim):
        # self.__dict__.update(stazione)
        self.id=stazione["id"]
        self.nome=stazione["nome"]
        self.tipo=stazione["tipo"]
        self.s=np.float64(stazione["s"])
        self.visite=np.float64(0)
        self.domande=np.float64(0)
        self.indici={'X':np.zeros(dim),'W':np.zeros(dim),'N':np.zeros(dim),'U':np.zeros(dim),'R':np.zeros(dim)}
        self.prob=[[0 for x in np.zeros(dim)]for y in np.zeros(dim)]

    def __getattr__(self, item):
        return 0

