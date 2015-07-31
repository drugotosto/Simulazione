__author__ = 'maury'

from simulatore.struttureDati.modello import *
from simulatore.simulatore import *

if __name__ == '__main__':

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello("parametri2.json")
    md.stampaStazioni()

    # Creazione del simulatore passandogli il modello appena creato
    sim=Simulatore(md)
    # Inizializzazione del simulatore
    sim.inizialization()
    # Esecuzione del simulatore
    sim.engine()
    # Resoconto degli indici per le diverse stazioni
    sim.report()

