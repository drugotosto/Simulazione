__author__ = 'maury'

from simulazione.struttureDati.modello import Modello
from simulazione.simulatore import Simulatore
from settaggiSim import *

if __name__ == '__main__':

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello(pathDati,debug)
    md.stampaStazioni()
    # Creazione del simulazione passandogli il modello appena creato
    sim=Simulatore(md)
    # Inizializzazione del simulazione con inserimento di "nj" job in coda alla stazione "indStaz" e tempo di terminazione della simulazione
    sim.inizialization(nj,tFine,indStaz)
    # Esecuzione del simulazione
    sim.engine(nj,tMax,indStaz,debug)
    # Resoconto degli indici per le diverse stazioni
    sim.report()
