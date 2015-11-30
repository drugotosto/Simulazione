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
        self.sommaTempiSim=np.float(0)
        self.sommaPartenzeStaz=[]
        self.visiteMedie=[]
        self.permMedie=[]
        self.tempoMedioCicl=np.float(0)
        self.varianzaTempoCicl=np.float(0)
        self.intervallo=[]
        self.precOttenuta=float(0)


    def azzeraValori(self):
        """
        Azzera i valori in merito alla somma dei tempi di simulazione e della somma delle partenze delle varie prove per ogni stazione
        :return:
        """
        self.sommaTempiSim=np.float(0)
        self.sommaPartenzeStaz=[]
        self.visiteMedie=[]
        self.permMedie=[]
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

    def calcoloStimatoreMedia(self):
        """
        Calcolo dello stimatore della media della mia v.c. utilizzando le prove fatte (da utilizzare per calcolarsi l'intervallo di confidenza)
        :return:
        """
        # Calcolo delle somme dei tempi di simulazione delle diverse prove 
        for prova in self.prove:
            self.sommaTempiSim+=prova.durataSim
        
        # Calcolo della somma delle diverse partenze fatte ad ogni simulazione per ciascuna stazione
        """for i in range(len(self.prove[0].partenzeStazioni)):
            for j,prova in enumerate(self.prove):
                if j==0:
                    self.sommaPartenzeStaz.append(prova.partenzeStazioni[i])
                else:
                    self.sommaPartenzeStaz[i]+=prova.partenzeStazioni[i]"""
        
        # Ciclo su tutte le prove fatte per calcolare visite medie (pesate) e tempi medi di permanenza (pesati) di tutte le stazioni
        for i in range(len(self.prove[0].partenzeStazioni)):
            for j,prova in enumerate(self.prove):
                    if (j==0):
                        self.visiteMedie.append((prova.partenzeStazioni[i]/prova.partenzeStazioni[sett.indStaz])*(prova.durataSim/self.sommaTempiSim))
                        self.permMedie.append((prova.areaStazioni[i]/prova.partenzeStazioni[i])*(prova.durataSim/self.sommaTempiSim))
                    else:
                        self.visiteMedie[i]+=(prova.partenzeStazioni[i]/prova.partenzeStazioni[sett.indStaz])*(prova.durataSim/self.sommaTempiSim)
                        self.permMedie[i]+=(prova.areaStazioni[i]/prova.partenzeStazioni[i])*(prova.durataSim/self.sommaTempiSim)

        # Calcolo del tempo di ciclo globale del sistema
        print "\n\nTEMPI MEDI PERMANENZA e VISITE/PARTENZE su",self.numProve,"prove fatte:"
        for i,permStaz in enumerate(self.permMedie):
            print "Stimatore puntuale del tempo medio (pesato) di permanenza della stazione",i,":",permStaz
            print "Le visite medie (pesate) fatte alla stazione",i,"e:",self.visiteMedie[i]
            self.tempoMedioCicl+=(self.visiteMedie[i]*permStaz)

        print "\nLo stimatore puntuale del tempo medio di ciclo mediato su tutte le prove:",self.tempoMedioCicl,"\n"
        tCicloMedio=float(0)
        for prova in self.prove:
            tCicloMedio+=prova.tempoMedioCiclTimeStamp*(prova.durataSim/self.sommaTempiSim)
        print "Lo stimatore puntuale del tempo medio di ciclo mediato su tutte le prove tramite \"time stap\":",tCicloMedio


    def calcolStimatoreVarianza(self):
        """
        Calcolo dello stimatore della varianza della mia v.c. utiizzando le prove fatte (da utilizzare per calcolarsi l'intervallo di confidenza)
        :return:
        """
        quadSommeDif=float(0)
        for prova in self.prove:
            quadSommeDif+=pow(prova.tempoMedioCicl-self.tempoMedioCicl,2)

        self.varianzaTempoCicl=sqrt(quadSommeDif/(self.numProve-1))

        
    def aggiornaIntervallo(self):
        """
        Controllo se ho raggiunto il livello di precisione richiesto tramite il numero di prove fatte
        :return:
        """
        # Calcolo i limiti dell'intervallo
        delta=stats.t.ppf(1-(sett.alfa/2),self.numProve-1)*(self.varianzaTempoCicl)/sqrt(self.numProve)
        self.intervallo.append(self.tempoMedioCicl-delta)
        self.intervallo.append(self.tempoMedioCicl+delta)

        print "\nIntervallo che ottengo: [",self.intervallo[0],",",self.intervallo[1],"]","con alfa=",sett.alfa

        # Controllo se sono riuscito a raggiungere la precisione richiesta
        self.precOttenuta=delta/self.tempoMedioCicl
        print "\nLa precisione richiesta e:",sett.precisione,". Quella che ottengo dopo",self.numProve,"prove effettuate e:",self.precOttenuta,"\n"

        for i,prova in enumerate(self.prove):
            print "Il numero di eventi generati nella",i,"prova sono:",prova.numEventi

        if self.precOttenuta>sett.precisione:
            # Calcolo il "presunto" numero di prove da dover ancora eseguire
            n1=pow(round(stats.t.ppf(1-(sett.alfa/2),self.numProve-1)*self.varianzaTempoCicl/(sett.precisione*self.tempoMedioCicl)),2)
            print "\nIl presunto numero di prove da effettuare per raggiungere la precisione risulta",n1
            # Aggiorno il numero di prove ancora da effettuare
            sett.proveN0=n1
            return True
        else:
            print "\nPRECISIONE RAGGIUNTA!!!"
            if self.intervallo[0]<=22.830389481<=self.intervallo[1]:
                sett.numSimDentro+=1
        return False



