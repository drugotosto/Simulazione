__author__ = 'maury'
"""
    Classe che preso in input il file json passato in input crea una lista di
    oggetti Stazione e memorizza la matrice di transione tra stazioni.
"""
import json
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


