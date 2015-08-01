__author__ = 'maury'

"""
    Classe che mi rappresenta la singola stazione con attributi recuperati dal file json + calcolati
    - parametri da file json
    - numero di jobs nella stazione
    - tempo di occupazione della stazione
    - area
    - arrivi
    - partenze
    - coda dei job alla stazione
    - indici di prestazione (X,W,N,U)
"""
from classTools import Display

class Stazione(Display):
    def __init__(self,stazione):
        self.__dict__.update(stazione)
        self.Njobs=0
        self.busyT=0.0
        self.area=0.0
        self.arrivi=0
        self.partenze=0
        self.coda=[]
        self.indici={'X':0.0,'W':0.0,'N':0.0,'U':0.0}

