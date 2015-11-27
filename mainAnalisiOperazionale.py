__author__ = 'maury'

"""
    MAIN PRINCIPALE
"""
from settaggi import *
from struttureDati import gestoreModello as gsm
from analisiOperazionale import *


if __name__=='__main__':
    print "\nAnalisi del modello analitico dato come progetto finale (modello di un sistema)"

    # Definzione #persone per cui si calcolano gli indici di prestazione

    # Costruzione del modello analitico preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=gsm.caricamentoModello("tracce/parametri.json")
    # Calcolo le visite del modello prendendo come riferiemento la stazione 0(terminali collegati)
    visite=calcoloVisite(md,indice_rif)
    print "\nLe visite fatte alle varie stazioni durante il periodo di osservazione T (Prendendo come riferimento la stazione 0) risultano essere: "
    for i,val in enumerate(visite):
        print "V",i,": ",val

    # Calcolo delle varie domande alle varie stazioni per capire quale e la stazione di bottleneck
    domande=calcoloDomande(md)
    print "\nDomande: ",domande

    # Calcolo il massimo della domanda per tutte quelle stazioni che non sono infinite server
    dMax=max(controlloStazione(md))
    b=[i for i, j in enumerate(domande) if j == dMax]
    print "La stazione con domanda maggiore=",dMax," risulta essere quella di indice:",b

    # Stampa delle stazioni
    # gsm.stampaStazioni(md)

    # Calcolo delle domande (V*S) cioe = tempo di permanenenza con una sola persona dentro
    som_domande=0
    for val in domande:
        som_domande+=val

    print "\n\n*****ANALISI ASINTOTICA DEL MODELLO******"
    print "Il Throughput massimo che il sistema puo raggiungere e dato dalla retta: y=",1/dMax
    print "L'asintoto obliquo che definisce la massima crescita del throughput del sistema" \
          " oltre al quale non e possibile andare risulta essere y: ", 1/(som_domande),"x"
    print "Il minimo tempo di risposta dato dal sistema (escludendo la stazione del terminali) e dato dalla retta: y=",som_domande-(md.stazioni[0].s*md.stazioni[0].visite)
    print "L'asintoto obliquo che definisce la minima crescita del che puo assumere il sistema (escludendo la stazione del terminali) possibile risulta essere y: ",dMax,"x -",(md.stazioni[0].s*md.stazioni[0].visite)
    print "L'asintoto obliquo della bottleneck",(md.stazioni[1].s*md.stazioni[1].visite),"x -",(md.stazioni[0].s*md.stazioni[0].visite)
    print "Ci si aspetta Utilizzazione Max della stazione di riferimento del: ",calcoloU(dMax,md,indice_rif),"%"

    # Chiamata per creazione grafico analisi asitotica di X e del tempo di risposta R (sul sistema)
    nStar=graficoAsintotico(dMax,som_domande,md)
    print "Il numero di jobs oltre al quale si andranno a formare le code sara: ",nStar
