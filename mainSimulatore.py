__author__ = 'maury'

from settaggiSim import *
from simulazione.struttureDati.transitorio import Transitorio
from simulazione.struttureDati.modello import Modello
from simulazione.simulatore import Simulatore
import datetime as dt

def avvioRunSimulazione(trans):
    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello(pathDati,debug)
    # md.stampaStazioni()
    # Creazione del simulazione passandogli il modello appena creato
    sim=Simulatore(md)
    # Inizializzazione del simulazione con inserimento di "nj" job in coda alla stazione "indStaz" e tempo di terminazione della simulazione
    sim.inizialization()
    # Esecuzione del simulazione
    sim.engine(trans)
    # Resoconto degli indici per le diverse stazioni
    # sim.report()


if __name__ == '__main__':

    now=dt.datetime.now()
    print "INIZIO:",now.strftime("%Y-%m-%d %H:%M")
    trans=Transitorio()
    while(trans.numProve<numRun):
        print "\n\n------------------- PROVA ",trans.numProve,"DI SIMULAZIONE"
        avvioRunSimulazione(trans)
        # Aggiorno campi Transitorio
        trans.indOss=0
        trans.numProve+=1

    trans.calcolaMediaVarianza()
    trans.stampaRisultati()
    now=dt.datetime.now()
    print "FINE:",now.strftime("%Y-%m-%d %H:%M")
