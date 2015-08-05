__author__ = 'maury'

"""
    Classe che definsice il cuore del simulatore che possiede come attributi
    - eventList: lista degli eventi futuri
    - freeList: lista degli eventi che possono essere riclicati
    - time: orologio del simulatore
    - md: modello del sistema reale che il simulatore prendera in considerazione
"""
from tools import *
from gestoreEventi import *
from struttureDati.evento import Evento
from struttureDati.distStazione import DistStazione,genDistrMisura
from struttureDati.modello import Modello


class Simulatore():
    def __init__(self,md,seme):
        """
        Costruttore del Simulatore che recupera il modello e il seme con cui inizializzare il generatore di numeri causuali
        :param md: Modello preso in considerazione dal file json
        :type md: Modello
        :param seme: seme iniziale con il quale inizializzare il generatore di num. casuali
        """
        self.eventList=[]
        self.freeList=[]
        self.time=0.0
        self.md=md
        self.listDistrStaz=[]
        for staz in md.stazioni:
            self.listDistrStaz.append(DistStazione(staz,seme))

    def inizialization(self,nj):
        """
        Schedula un job nella future event list in uscita dalla stazione "0" piu "tot" job in coda alla stazione 0
        :param nj: numero di job da inserire in coda alla stazione 0
        """
        # Genero una istanza del tempo di servizio della stazione 0
        servT=self.listDistrStaz[0].genDistr()
        # Schedulo una partenza dalla stazione 0
        schedula(self.eventList,Evento(self.time,servT,servT,"partenza",1,0))
        # Schedulo un arrivo alla stazione 1
        schedula(self.eventList,Evento(self.time,-1,servT,"arrivo",1,1))
        for i in range(2,nj+2):
            # Genero una istanza del tempo di servizio della stazione 0
            servT=self.listDistrStaz[0].genDistr()
            # Schedulo un job in coda alla stazione 0
            accoda(self.md.stazioni[0],Evento(self.time,servT,-1,"coda",i,0))
        # Schedulo un evento misura per la stampa dei vari indici delle stazioni
        schedula(self.eventList,Evento(self.time,-1,genDistrMisura(self.time+2),"misura",-1,-1))
        # Schedulo evento fine simulazione
        schedula(self.eventList,Evento(self.time,-1,500,"fine",-1,-1))
        print "\nFUTURE LIST:",self.eventList,"\n"

    def engine(self):
        # Dizionario che simula lo "switch" per richiamare la funzione adeguata all gestione dell'evento
        tipoEv={"arrivo":arrivo,"partenza":partenza,"misura":misura,"fine":fine}
        goOn=True
        while goOn:
            ev=recProxEvento(self.eventList)
            """:type : Evento"""
            self.time=ev.occT
            goOn=tipoEv[ev.tipo](self)
            print "FUTURE LIST:",self.eventList
        # num=self.listDistrStaz[1].genDistr()
        # print "NUM",num
        # Stampa delle distribuzioni che compongono il tempo di servizio di una stazione
        # self.listDistrStaz[0].stampaDistr()
        # chooseRoute(self.md.q[1])

    def report(self):
        pass
