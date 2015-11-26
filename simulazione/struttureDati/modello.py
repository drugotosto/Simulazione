__author__ = 'maury'
"""
    Classe che preso in input il file json passato in input crea una lista di
    oggetti Stazione e memorizza la matrice di transione tra stazioni.
"""
import json
import numpy as np
from simulazione.struttureDati.stazione import Stazione

class Modello():
    def __init__(self,pathDati,debug):
        """
        Costruttore del Modello dato in input attraverso il file json
        :param pathDati: Percorso del file json dal quale recuperare i dati
        :type path: file
        :param stazioni: Lista delle varie stazioni che compongono il modello
        :type stazioni: list
        """
        with open(pathDati) as file:
            model = json.loads(file.read())
        self.stazioni=[]
        # Lista di dizioniari che verra trasormata in una lista di oggetti Stazione
        for staz in model["stazioni"]:
            """:type : Stazione"""
            self.stazioni.append(Stazione(staz,debug))
        self.q=model["q"]

    def stampaStazioni(self):
        print "\n"
        for staz in  self.stazioni:
            print "Stazione ",staz.id,": ",vars(staz)


    def azzeraValoriStazioni(self):
        for staz in self.stazioni:
            staz.tCicloJob=float(0)
            staz.tMedioCicloJob=float(0)
            staz.tPartenza=float(0)
            staz.tArrivo=float(0)
            staz.visite=float(0)
            staz.Njobs=np.float(0)
            staz.busyT=np.float(0)
            staz.area=np.float(0)
            staz.arrivi=np.float(0)
            staz.partenze=np.float(0)
            staz.nMax=0
            staz.coda=[]
            staz.indici={'X':np.float(0),'W':np.float(0),'N':np.float(0),'U':np.float(0)}