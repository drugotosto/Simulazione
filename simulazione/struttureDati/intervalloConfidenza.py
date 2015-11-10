__author__ = 'maury'

import numpy as np

class IntervalloConfidenza():
    def __init__(self):
        """
        Costruttore dell'intervallo di confidenza
        :param numProve: Num
        """
        self.numProve=1
        # Lista degi vari dati delle differenti prove fatte
        self.prove=[]
        self.sommaArea=np.float(0)
        self.sommaPatenze=np.float(0)
        self.media=np.float(0)
        self.varianza=np.float(0)


    def salvaDatiProva(self, prova):
        """
        Aggiunge la prova fatta alla lista delle prove eseguite per il calcolo dell'intervallo
        :param prova:
        :return:
        """
        self.numProve+=1
        self.prove.append(prova)

    def calcoloStimatoreMedia(self):
        pass

    def calcolStimatoreVarianza(self):
        pass

    def aggiornaIntervallo(self):
        return

