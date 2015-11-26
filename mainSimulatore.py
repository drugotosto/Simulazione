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

    count=0
    while count<100:
        sett.proveN0=3
        print "\n\n*************************************************SIMULAZIONE",count+1
        inizio=dt.datetime.now()
        continuaSim=True
        # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
        md=Modello(sett.pathDati,sett.debug)
        # Costruisco un intervallo di Confidenza
        inter=IntervalloConfidenza()
        while(continuaSim):
            inter.azzeraValori()
            while(inter.numProve<sett.proveN0):
                print "\n\n------------------- PROVA",inter.numProve+1,"DI SIMULAZIONE"
                md.azzeraValoriStazioni()
                prova=avvioRunSimulazione(md)
                inter.aggiungiDatiProva(prova)

            inter.calcoloStimatoreMedia(md)
            inter.calcolStimatoreVarianza()
            # Controllo se il  numero di prove effettuate e sufficiente per temrminare il calcolo dell'intervallo e aggiorna tale valore nel caso
            continuaSim=inter.aggiornaIntervallo()
        fine=dt.datetime.now()
        print "\nNJ:",sett.nj," - tFine:",sett.tFine," - tMax",sett.tMax," - debug:",sett.debug," - #ProveEffettuate:",sett.proveN0," - TempFineTrans:",sett.fineTrans," - pathDati:",sett.pathDati
        print "\nINIZIO:",inizio.strftime("%Y-%m-%d %H:%M")
        print "\nFINE:",fine.strftime("%Y-%m-%d %H:%M")
        count+=1
    print "Il numero di prove di Simulazione in cui il valore teorico e dentro all'intervallo:",sett.numSimDentro
