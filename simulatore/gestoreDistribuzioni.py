__author__ = 'maury'

"""
    Classe che permette di generare le istanze di variabili
    casuali delle diverse distribuzioni di cui si necessita
"""
from struttureDati.distStazione import DistStazione

class GestDistr():
    def __init__(self,md,seme):
        self.listDistrStaz=[]
        for staz in md.stazioni:
            self.listDistrStaz.append(DistStazione(staz,seme))

    # Restituisce una istanza di v.c. Uniforme
    def unifor(self):
        pass

    # Restituisce una istanza di v.c. Esponenziale
    def exp(self):
        pass

    # Restituisce una istanza di v.c. Erlang_k
    def erlg(self):
        pass

    # Restituisce una istanza di v.c. Normale
    def norm(self):
        pass
