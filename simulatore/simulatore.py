__author__ = 'maury'

"""
    Classe che definsice il cuore del simulatore che possiede come attributi
    - eventList: lista degli eventi futuri
    - freeList: lista degli eventi che possono essere riclicati
    - time: orologio del simulatore
    - md: modello del sistema reale che il simulatore prendera in considerazione
"""
# from simulatore.struttureDati.evento import Evento
from struttureDati.distStazione import DistStazione

class Simulatore():
    def __init__(self,md,seme):
        self.eventList=[]
        self.freeList=[]
        self.time=0.0
        self.md=md
        self.listDistrStaz=[]
        for staz in md.stazioni:
            self.listDistrStaz.append(DistStazione(staz,seme))

    def inizialization(self):
        pass

    def engine(self):
        num=self.listDistrStaz[1].genDistr()
        print "NUM:",num
        # Stampa delle distribuzioni che compongono il tempo di servizio di una stazione
        self.listDistrStaz[1].stampaDistr()
        pass

    def report(self):
        pass