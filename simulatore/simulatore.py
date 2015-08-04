__author__ = 'maury'

"""
    Classe che definsice il cuore del simulatore che possiede come attributi
    - eventList: lista degli eventi futuri
    - freeList: lista degli eventi che possono essere riclicati
    - time: orologio del simulatore
    - md: modello del sistema reale che il simulatore prendera in considerazione
"""
from gestoreEventi import *
from simulatore.struttureDati.evento import Evento
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

    # Schedula un job nella future event list in uscita dalla stazione 0 pi tot job in coda alla stazione 0
    def inizialization(self,nj):
        # Genero una istanza del tempo di servizio della stazione 0
        servT=self.listDistrStaz[0].genDistr()
        # Schedulo una partenza dalla stazione 0
        schedula(self.eventList,Evento(0.0,servT,servT,"partenza",1,0))
        for i in range(2,nj+2):
            # Genero una istanza del tempo di servizio della stazione 0
            servT=self.listDistrStaz[0].genDistr()
            # Schedulo tot job in coda alla stazione 0
            accoda(self.md.stazioni[0],Evento(0.0,servT,0,'coda',i,0))
        pass

    def engine(self):
        num=self.listDistrStaz[1].genDistr()
        # Stampa delle distribuzioni che compongono il tempo di servizio di una stazione
        # self.listDistrStaz[1].stampaDistr()
        # chooseRoute(self.md.q[1])

    def report(self):
        pass