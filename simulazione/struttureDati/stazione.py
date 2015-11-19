__author__ = 'maury'

"""
    Classe che mi rappresenta la singola stazione con attributi recuperati dal file json + calcolati
"""
import numpy as np
from simulazione.struttureDati.servizio import Servizio

class Stazione():
    def __init__(self,staz,debug):
        """
        Costruttore della stazione
        :param staz: Dizionario che rappresenta la stazione
        :type staz: dict
        :param servizio: Definisce la distribuzione del tempo di servizio della stazione (contiene cioe la lista delle diverse distribuzioni che lo compongono nel caso di 'server') 
        :type DistStazione
        """
        # self.__dict__.update(staz)
        self.id=staz["id"]
        self.nome=staz["nome"]
        self.tipo=staz["tipo"]
        self.Njobs=np.float(0)
        self.busyT=np.float(0)
        self.area=np.float(0)
        self.arrivi=np.float(0)
        self.partenze=np.float(0)
        self.nMax=0
        self.coda=[]
        self.indici={'X':np.float(0),'W':np.float(0),'N':np.float(0),'U':np.float(0)}
        self.servizio=Servizio(staz)

    def genTempSer(self):
        if self.tipo=="infinite":
            return self.servizio.genDistrIF()
        else:
            return self.servizio.genDistr()

    def stampaDistr(self):
        self.servizio.stampaDistr()

    def fineTransitorio(self):
        """
        Resetto tutti i campi della stazione
        :return:
        """
        self.busyT=np.float(0)
        self.area=np.float(0)
        self.arrivi=np.float(0)
        self.partenze=np.float(0)
        self.nMax=0
        self.indici={'X':np.float(0),'W':np.float(0),'N':np.float(0),'U':np.float(0)}