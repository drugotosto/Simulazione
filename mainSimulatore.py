__author__ = 'maury'

from simulazione.struttureDati.modello import Modello
from simulazione.simulatore import Simulatore
from simulazione.struttureDati.intervalloConfidenza import IntervalloConfidenza
from simulazione.struttureDati.prova import Prova
import settaggiSim as sett
import datetime as dt

def avvioRunSimulazione(md):
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

    now=dt.datetime.now()
    print "\nNJ:",sett.nj," - tFine:",sett.tFine," - tMax",sett.tMax," - debug:",sett.debug," - #ProveIniziali:",sett.proveN0," - TempFineTrans:",sett.fineTrans," - pathDati:",sett.pathDati
    print "\nINIZIO:",now.strftime("%Y-%m-%d %H:%M")
    continuaSim=True
    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=Modello(sett.pathDati,sett.debug)
    # Costruisco un intervallo di Confidenza
    inter=IntervalloConfidenza()
    while(continuaSim):
        while(inter.numProve<sett.proveN0):
            print "\n\n------------------- PROVA",inter.numProve+1,"DI SIMULAZIONE"
            md.azzeraValoriStazioni()
            prova=avvioRunSimulazione(md)
            inter.aggiungiDatiProva(prova)

        inter.calcoloStimatoreMedia()
        inter.calcolStimatoreVarianza()
        # Controllo se il  numero di prove effettuate e sufficiente per temrminare il calcolo dell'intervallo e aggiorna tale valore nel caso
        continuaSim=inter.aggiornaIntervallo()
    now=dt.datetime.now()
    print "\nFINE:",now.strftime("%Y-%m-%d %H:%M")
