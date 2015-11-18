__author__ = 'maury'

from simulazione.struttureDati.modello import Modello
from simulazione.simulatore import Simulatore
from simulazione.struttureDati.intervalloConfidenza import IntervalloConfidenza
from simulazione.struttureDati.prova import Prova
import settaggiSim as sett

def avvioRunSimulazione():
    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello(sett.pathDati,sett.debug)
    # md.stampaStazioni()
    # Creazione del simulazione passandogli il modello appena creato
    sim=Simulatore(md)
    # Inizializzazione del simulazione con inserimento di "nj" job in coda alla stazione "indStaz" e tempo di terminazione della simulazione
    sim.inizialization()
    # Esecuzione del simulazione
    sim.engine()
    # Resoconto degli indici per le diverse stazioni
    sim.report()
    # Crea una nuova prova
    prova=Prova()
    # Registra indici e dati della prova
    prova.registraDatiProva(sim)
    return prova

if __name__ == '__main__':

    continuaSim=True
    inter=IntervalloConfidenza()
    while(continuaSim):
        while(inter.numProve<sett.proveN0):
            print "\n\n------------------- PROVA ",inter.numProve,"DI SIMULAZIONE"
            prova=avvioRunSimulazione()
            inter.aggiungiDatiProva(prova)

        inter.calcoloStimatoreMedia()
        inter.calcolStimatoreVarianza()
        # Controllo se il  numero di prove effettuate e sufficiente per temrminare il calcolo dell'intervallo e aggiorna tale valore nel caso
        continuaSim=inter.aggiornaIntervallo()