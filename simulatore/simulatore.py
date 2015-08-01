__author__ = 'maury'

"""
    Classe che definsice il cuore del simulatore che possiede come attributi
    - eventList: lista degli eventi futuri
    - freeList: lista degli eventi che possono essere riclicati
    - time: orologio del simulatore
    - md: modello del sistema reale che il simulatore prendera in considerazione
"""
# from simulatore.struttureDati.evento import Evento
from gestoreDistribuzioni import GestDistr

class Simulatore():
    def __init__(self,md):
        self.eventList=[]
        self.freeList=[]
        self.time=0.0
        self.md=md
        self.gestDist=GestDistr(md,seme=1)

    def inizialization(self):
        pass

    def engine(self):
        pass

    def report(self):
        pass