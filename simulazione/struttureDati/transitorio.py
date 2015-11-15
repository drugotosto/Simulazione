__author__ = 'maury'

import numpy as np

class Transitorio():
    def __init__(self):
        self.numProve=0
        self.indOss=0
        self.listaOss=[]

    def calcolaMediaVarianza(self):
        """
        Vado a calcolare medie e varianze campionarie sui vari indici delle diverse prove e
        per le diverse stazioni, rilevati al momento delle diverse osservazioni
        :return:
        """
        # Memorizzo la somma complessiva dei vari indici, di ogni stazione, per le varie osservazioni
        for oss in self.listaOss:
            for prova in oss.indiciProve:
                for i in range(4):
                    for j,indStaz in enumerate(prova.indiciStazioni):
                        if j==i:
                            oss.sommeIndici[i]["SommaX"]+=indStaz["X"]
                            oss.sommeIndici[i]["SommaN"]+=indStaz["N"]

        """
        DEVO CALCOLARMI LE MEDIE E VARIANZE DELLE VARIE OSSERVAZIONI
        """

    def stampaRisultati(self):
        """
        Stampa gli scarti delle medie delle varie osservazioni con relativa varianza
        :return:
        """
        pass
