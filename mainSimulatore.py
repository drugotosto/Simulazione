__author__ = 'maury'

from simulatore.struttureDati.modello import Modello
from simulatore.simulatore import Simulatore

if __name__ == '__main__':

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello("parametri4.json")
    md.stampaStazioni()
    seme="debug"

    # Creazione del simulatore passandogli il modello appena creato
    sim=Simulatore(md,seme)
    # Inizializzazione del simulatore
    sim.inizialization()
    # Esecuzione del simulatore
    sim.engine()
    # Resoconto degli indici per le diverse stazioni
    sim.report()
