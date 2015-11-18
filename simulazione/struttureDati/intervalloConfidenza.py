__author__ = 'maury'

import numpy as np
import settaggi as sett

class IntervalloConfidenza():
    def __init__(self):
        """
        Costruttore dell'intervallo di confidenza
        :param numProve: Num
        """
        self.numProve=0
        # Lista degi vari dati delle differenti prove fatte
        self.prove=[]
        self.sommaAreeStaz=[]
        self.sommaPatenzeStaz=[]
        self.sommaAreaStazQuad=[]
        self.sommaPatenzeStazQuad=[]
        self.sommaAreaPartenzeStaz=[]
        self.mediaStaz=[]
        self.varianza=[]
        self.tempoCicl=np.float(0)

    def aggiungiDatiProva(self, prova):
        """
        Aggiunge la prova fatta alla lista delle prove eseguite per il calcolo dell'intervallo
        :param prova:
        :return:
        """
        self.numProve+=1
        self.prove.append(prova)

    def calcoloStimatoreMedia(self):
        """
        Calcolo dello stimatore della media della mia v.c. utilizzando le prove fatte (da utilizzare per calcolarsi l'intervallo di confidenza)
        :return:
        """
        # Ciclo su tutte le stazioni
        for i in range(len(self.prove[0].partenzeStazioni)):
            # Ciclo su tutte le prove fatte
            for j,prova in enumerate(self.prove):
                if (j==0):
                    self.sommaAreeStaz.append(prova.areaStazioni[i])
                    self.sommaPatenzeStaz.append(prova.partenzeStazioni[i])
                else:
                    self.sommaAreeStaz[i]+=prova.areaStazioni[i]
                    self.sommaPatenzeStaz[i]+=prova.partenzeStazioni[i]
        
        # Calcolo lo stimatore puntuale della media del tempo di permanenza per le varie stazioni
        self.mediaStaz=[sommaArea/sommaPartenza for sommaArea,sommaPartenza in zip(self.sommaAreeStaz,self.sommaPatenzeStaz)]

        # Calcolo del tempo di ciclo globale del sistema
        for perm in self.mediaStaz:
            self.tempoCicl+=perm

        print "\nTEMPI MEDI PERMANENZA su",self.numProve,"fatte:"
        for i,perm in enumerate(self.mediaStaz):
            print "Tempo medio di permanenza stazione",i,":",perm

        print "Lo stimatore puntuale del tempo medio di ciclo e:",self.tempoCicl

    def calcolStimatoreVarianza(self):
        """
        Calcolo dello stimatore della varianza della mia v.c. utiizzando le prove fatte (da utilizzare per calcolarsi l'intervallo di confidenza)
        :return:
        """
        pass

    def aggiornaIntervallo(self):
        """
        Controllo se ho raggiunto il livello di precisione richiesto tramite il numero di prove fatte
        :return:
        """
        # Aggiorno il numero delle prove da fare nel caso...
        # sett.proveN0=
        return False

