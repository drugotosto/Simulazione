__author__ = 'maury'

import numpy as np
from math import sqrt
import settaggiSim as sett
from scipy import stats

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
        self.sommaVisite=[]
        self.sommaPatenzeStaz=[]
        self.sommaAreaStazQuad=[]
        self.sommaPatenzeStazQuad=[]
        self.sommaAreaPartenzeStaz=[]
        self.mediaStaz=[]
        self.visiteMedie=[]
        self.varianza=[]
        self.sommaMediePartStaz=float(0)
        self.tempoMedioCicl=np.float(0)
        self.varianzaTempoCicl=np.float(0)
        self.intervallo=[]
        self.precOttenuta=float(0)



    def aggiungiDatiProva(self, prova):
        """
        Aggiunge la prova fatta alla lista delle prove eseguite per il calcolo dell'intervallo
        :param prova:
        :return:
        """
        self.numProve+=1
        self.prove.append(prova)

    def calcoloStimatoreMedia(self,md):
        """
        Calcolo dello stimatore della media della mia v.c. utilizzando le prove fatte (da utilizzare per calcolarsi l'intervallo di confidenza)
        :return:
        """
        # Ciclo su tutte le stazioni
        for i in range(len(self.prove[0].partenzeStazioni)):
            # Ciclo su tutte le prove fatte per andare a salvarmi dei valori che poi andranno ad essere utilizzati nel calcolo dell'intervallo di confidenza
            for j,prova in enumerate(self.prove):
                if (j==0):
                    self.sommaAreeStaz.append(prova.areaStazioni[i])
                    self.sommaAreaStazQuad.append(pow(prova.areaStazioni[i],2))
                    self.sommaPatenzeStaz.append(prova.partenzeStazioni[i])
                    self.sommaPatenzeStazQuad.append(pow(prova.partenzeStazioni[i],2))
                    self.sommaAreaPartenzeStaz.append(prova.areaStazioni[i]*prova.partenzeStazioni[i])
                    self.sommaVisite.append(prova.partenzeStazioni[i])
                else:
                    self.sommaAreeStaz[i]+=prova.areaStazioni[i]
                    self.sommaAreaStazQuad[i]+=pow(prova.areaStazioni[i],2)
                    self.sommaPatenzeStaz[i]+=prova.partenzeStazioni[i]
                    self.sommaPatenzeStazQuad[i]+=pow(prova.partenzeStazioni[i],2)
                    self.sommaAreaPartenzeStaz[i]+=(prova.areaStazioni[i]*prova.partenzeStazioni[i])
                    self.sommaVisite[i]+=prova.partenzeStazioni[i]
        
        # Calcolo lo stimatore puntuale della media del tempo di permanenza per le varie stazioni
        self.mediaStaz=[sommaArea/sommaPartenza for sommaArea,sommaPartenza in zip(self.sommaAreeStaz,self.sommaPatenzeStaz)]
        self.visiteMedie=[sommaVisiteStaz/self.numProve for sommaVisiteStaz in self.sommaVisite]

        # Calcolo del tempo di ciclo globale del sistema
        print "\n\nTEMPI MEDI PERMANENZA e VISITE su",self.numProve,"fatte:"
        for i,permStaz in enumerate(self.mediaStaz):
            self.tempoMedioCicl+=(self.visiteMedie[i]*permStaz)
            print "Stimatore puntuale del tempo medio di permanenza della stazione",i,":",permStaz
            print "Gli arrivi/visite medie fatte alla stazione",i,"e:",self.visiteMedie[i]

        print "\nLo stimatore puntuale del tempo medio di ciclo e:",self.tempoMedioCicl

    def calcolStimatoreVarianza(self):
        """
        Calcolo dello stimatore della varianza della mia v.c. utiizzando le prove fatte (da utilizzare per calcolarsi l'intervallo di confidenza)
        :return:
        """
        for i in range(len(self.mediaStaz)):
            self.varianza.append(sqrt((self.sommaAreaStazQuad[i]-(2*self.mediaStaz[i]*self.sommaAreaPartenzeStaz[i])+(pow(self.mediaStaz[i],2)*self.sommaPatenzeStazQuad[i]))/(self.numProve-1)))
            self.varianzaTempoCicl+=self.varianza[i]

    def aggiornaIntervallo(self):
        """
        Controllo se ho raggiunto il livello di precisione richiesto tramite il numero di prove fatte
        :return:
        """
        # Calcolo la somma delle medie delle partenze di tutte le stazioni
        for somma in self.sommaPatenzeStaz:
            media=somma/self.numProve
            self.sommaMediePartStaz+=media

        # Calcolo i limiti dell'intervallo
        delta=stats.t.ppf(1-(sett.alfa/2),self.numProve-1)*(self.varianzaTempoCicl)/(sqrt(self.numProve)*self.sommaMediePartStaz)
        self.intervallo.append(self.tempoMedioCicl-delta)
        self.intervallo.append(self.tempoMedioCicl+delta)

        print "\nIntervallo che ottengo: [",self.intervallo[0],",",self.intervallo[1],"]","con alfa=",sett.alfa

        # Controllo se sono riuscito a raggiungere la precisione richiesta
        self.precOttenuta=delta/self.tempoMedioCicl
        print "\nLa precisione richiesta e:",sett.precisione,". Quella che ottengo dopo",self.numProve,"prove effettuate e:",self.precOttenuta

        if self.precOttenuta>sett.precisione:
            # Calcolo il "presunto" numero di prove da dover ancora eseguire
            n1=pow(round(stats.t.ppf(1-(sett.alfa/2),self.numProve-1)*self.varianzaTempoCicl/(sett.precisione*self.tempoMedioCicl*self.sommaMediePartStaz)),2)
            print "\nIl presunto numero di prove da effettuare per raggiungere la precisione risulta",n1
            # Aggiorno il numero di prove ancora da effettuare
            sett.proveN0=n1
        else:
            print "\nPRECISIONE RAGGIUNTA!!!"
        return False

