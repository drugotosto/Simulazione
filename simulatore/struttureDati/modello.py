__author__ = 'maury'
"""
    Classe che preso in input il file json passato in input crea una lista di
    oggetti Stazione e memorizza la matrice di transione tra stazioni.
"""
import json
from simulatore.struttureDati.stazione import Stazione

class Modello():
    def __init__(self,path):
        """
        Costruttore del Modello dato in input attraverso il file json
        :param path: Percorso del file json dal quale recuperare i dati
        :type path: file
        """
        with open(path) as file:
            model = json.loads(file.read())
        self.stazioni=[]
        # Lista di dizioniari che verra trasormata in una lista di oggetti Stazione
        for staz in model["stazioni"]:
            """:type : Stazione"""
            self.stazioni.append(Stazione(staz))
        self.q=model["q"]

    def stampaStazioni(self):
        for staz in  self.stazioni:
            print "Stazione ",staz.id,": ",staz


