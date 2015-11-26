__author__ = 'maury'

import settaggiSim as sett
import numpy as np

class Prova():
    def __init__(self):
        """
        Costruttore di una singola prova eseguita
        :return:
        """
        self.areaStazioni=[]
        self.partenzeStazioni=[]
        self.arriviStazioni=[]
        self.durataSim=np.float(0)
        self.permMedie=[]
        self.tempoMedioCicl=np.float(0)
        self.varianzaTempoCicl=np.float(0)
        self.tempoMedioCiclTimeStamp=float(0)

    def registraDatiProva(self,sim):
        """
        Vado a registrare per tutte le stazioni i valori di Arrivi,Partenze,durata di simulazione
        :return:
        """
        self.areaStazioni=[staz.area for staz in sim.md.stazioni]
        self.partenzeStazioni=[staz.partenze for staz in sim.md.stazioni]
        self.arriviStazioni=[staz.arrivi for staz in sim.md.stazioni]
        self.durataSim=sim.time-sett.fineTrans
        self.tempoMedioCiclTimeStamp=sim.md.stazioni[sett.indStaz].tMedioCicloJob


        # Calcolo i tempi medi di permanenza di tutte le stazioni
        for i in range(len(self.partenzeStazioni)):
            self.permMedie.append(self.areaStazioni[i]/self.partenzeStazioni[i])

        # Calcolo del tempo di ciclo globale del sistema
        for i,permStaz in enumerate(self.permMedie):
            self.tempoMedioCicl+=((self.partenzeStazioni[i]/self.partenzeStazioni[sett.indStaz])*permStaz)