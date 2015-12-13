__author__ = 'maury'

"""
    MAIN PRINCIPALE
"""
from settaggi import *
from cateneMarkov import *
from struttureDati import gestoreModello as gsm
from analisiOperazionale import *

if __name__=='__main__':
    print "Costruzione catena di Markov del modello dato come progetto finale (modello di un sistema)\n"

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=gsm.caricamentoModello("tracce/parametri.json")

    # Stampa delle stazioni
    # gsm.stampaStazioni(md)

    # Calcolo le visite del modello prendendo come riferiemento la stazione 0(terminali collegati)
    visite=calcoloVisite(md,indice_rif)

    for n in range(1,n+1):
        print "\n\nCASO N=",n,"*********************************"
        # Generazione dello spazio degli stati
        spazio=generaSpazioStati(md,n)

        print "Spazio Erlang:",spazio,"\nnumero:",len(spazio)

        # Dizionario con  K=0,1,2,... V="Stato/StatoErlang"
        spazioStati={i:stat for i,stat in enumerate(spazio)}

        # Aggiunta dello spazio degli stati al modello
        gsm.aggiungiSpazio(md,spazioStati,n)

        print "Spazio deglis stati:",md.spazioStati
        print "Lunghezza Spazio degli stati: ",len(md.spazioStati)

        # Chiamata per la creazione della matrice Q
        q=creazioneMatriceQ(md)

        print "\nLA MATRICE Q risulta essere:\n",q
        print "La somma per righe e:",map(sum,q),"\nlunghezza",len(q)

        # Chiamata per la risoluzione del sistema
        piG=risoluzioneSistema(q)

        print "\nLa distribuzione di prob dei vari stati risulta essere: \n",piG,"\ndi lunghezza:",len(piG),"con somma di:",sum(piG),"\n"

        # Settaggio delle varie P(k,n) per le diverse stazioni al variare del num. persone nel sistema
        preparazioneCalcoloIndici(md,piG,n)

    # Calcolo degli indici veri e propri
    calcoloIndici(md)


