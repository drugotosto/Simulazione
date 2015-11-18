__author__ = 'maury'

"""
    Classe che definsice il cuore del simulazione che possiede come attributi
    - eventList: lista degli eventi futuri
    - freeList: lista degli eventi che possono essere riclicati
    - time: orologio del simulazione
    - md: modello del sistema reale che il simulazione prendera in considerazione
"""
from settaggiSim import *
from simulazione.gestoreEventi import *
from struttureDati.evento import Evento
from struttureDati.servizio import genTempMisura
from struttureDati.modello import Modello
from simulazione.struttureDati.servizio import generaSeme
import numpy as np
import random as ran

class Simulatore():
    def __init__(self,md):
        """
        Costruttore del Simulatore che recupera il modello e setta o meno un
        seme di debug con cui inizializzare il generatore di numeri causuali
        :param md: Modello preso in considerazione dal file json
        :type md: Modello
        :param seme: seme iniziale con il quale inizializzare il generatore di num. casuali
        """
        self.eventList=[]
        self.freeList=[]
        self.time=np.float(0)
        self.md=md

    def inizialization(self):
        """
        Schedula un job nella future event list in uscita dalla stazione "indStaz"
        piu "tot" job in coda alla stazione "IndStaz" , un evento di misurazione
        e un evento di fine simulazione
        :param nj: numero di job da inserire in coda alla stazione 0
        """
        # Genero una istanza del tempo di servizio e schedulo una partenza dalla stazione "indStaz"
        servT=self.md.stazioni[indStaz].genTempSer()
        schedula(self.eventList,Evento(self.time,servT,servT,"partenza",1,indStaz))
        for i in range(2,nj+2):
            servT=self.md.stazioni[indStaz].genTempSer()
             # Nel caso la stazione di partenza non fosse un I.S. allora accodo gli altri jobs
            if self.md.stazioni[indStaz].tipo!="infinite":
                accoda(self.md.stazioni[indStaz],Evento(self.time,servT,-1,"coda",i,indStaz))
            else:
                schedula(self.eventList,Evento(self.time,servT,servT,"partenza",i,indStaz))
        self.md.stazioni[indStaz].Njobs=nj+1
        self.md.stazioni[indStaz].nMax=nj+1
        # Schedulo un evento misura per la stampa dei vari indici delle stazioni
        schedula(self.eventList,Evento(self.time,-1,genTempMisura(self.time+2),"misura",-1,-1))
        # Schedulo evento fine simulazione
        schedula(self.eventList,Evento(self.time,-1,tFine,"fine",-1,-1))
        # Schedulo il fine transitorio (azzeramento dei valori recuperati)
        schedula(self.eventList,Evento(self.time,-1,fineTrans,"fineTransizione",-1,-1))

    def engine(self):
        """
        Motore del simulatore
        """
        # Dizionario che simula lo "switch" per richiamare la funzione adeguata all gestione dell'evento
        tipoEv={"arrivo":arrivo,"partenza":partenza,"misura":misura,"fine":fine,"fineTransizione":fineTransizione}
        goOn=True
        okStop=False
        # Istanzio un generatore di numeri casuali utilizzato per il routing degli eventi
        route=ran.Random()
        route.seed(generaSeme())
        while goOn:
            # Recupero prox evento dalla FUTURE EVENT LIST
            ev=recProxEvento(self.eventList)
            oldTime=self.time
            """:type : Evento"""
            self.time=ev.occT
            # stampaSituazione(self,self.time)
            interval=np.float(self.time-oldTime)
            # Termino se ho gia superato la fine simulazione e sono in E.O. o se cmq ho superato la soglia massima
            if (okStop and controlloFine(self,ev,nj,indStaz))or(self.time>=tMax):
                if self.time<tMax:
                    print "\nSONO USCITO IN E.O."
                else:
                    print "\nSONO USCITO PER EVITARE LOOP"
                goOn=False
            else:
                # Aggiorno le statistiche delle stazioni
                for staz in self.md.stazioni:
                    if staz.Njobs>0:
                        staz.busyT+=interval
                        staz.area+=np.float(interval*staz.Njobs)
                        if staz.Njobs>staz.nMax:
                            staz.nMax=staz.Njobs
                # Richiamo la procedura opportuna per la gestione dell'evento considerato
                okStop=tipoEv[ev.tipo](self,ev,okStop,route)
                restituisci(self.freeList,ev)

        # Stampa delle distribuzioni che compongono il tempo di servizio di una stazione
        # self.md.stazioni[1].stampaDistr()

    def report(self):
        """
        Reportistica finale sui vari indice di prestazione
        """
        print "\n\nREPORTISTICA FINE SIMULAZIONE"
        # stampaSituazione(self,self.time)
        calcoloStampaIndici(self)


