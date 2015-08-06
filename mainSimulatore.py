__author__ = 'maury'

from simulazione.struttureDati.modello import Modello
from simulazione.simulatore import Simulatore

if __name__ == '__main__':

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello("parametri2.json")
    md.stampaStazioni()
    seme="debug"

    # Creazione del simulazione passandogli il modello appena creato
    sim=Simulatore(md,seme)
    # Inizializzazione del simulazione con inserimento di "nj" job in coda alla stazione 0 e tempo di terminazione della simulazione
    sim.inizialization(nj=2,tFine=550)
    # Esecuzione del simulazione
    sim.engine()
    # Resoconto degli indici per le diverse stazioni
    sim.report()
