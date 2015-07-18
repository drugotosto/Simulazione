__author__ = 'maury'

"""
    MAIN PRINCIPALE
"""
import numpy as np
from settaggi import *
from cateneMarkov import *
from struttureDati import gestoreModello as gsm

if __name__=='__main__':
    print "Costruzione catena di Markov del modello dato come progetto finale (modello di un sistema)\n"

    # Costruzione del modello preso in esame da un file json da cui si recuperano i parametri in ingresso
    md=gsm.caricamentoModello("parametri.json")

    for n in range(1,n+1):
        # Generazione dello spazio degli stati
        spazio=generaSpazioStati(n)

        """if (11,0,2,2) in spazio:
            print "Presente"
        else:
            print "Assente"
        print "spazio:",spazio,"\nnumero:",len(spazio)"""

        # Dizionario con indice numerico 0,1,2,... con valori tuple formate da: ((n,n,n,n),'(n,n,n,n)')
        spazioStati={i:(stat,str(stat)) for i,stat in enumerate(spazio)}

          # Aggiunta dello spazio degli stati al modello
        gsm.aggiungiSpazio(md,spazioStati,n)

        print "\n\nCASO N=",n,"*********************************"
        print "Spazio deglis stati:",md.spazioStati
        print "Lunghezza Spazio degli stati: ",len(md.spazioStati)

        # Chiamata per la creazione della matrice Q
        q=creazioneMatriceQ(md)

        print "\nLA MATRICE Q risulta essere:\n",q

        # Chiamata per la risoluzione del sistema
        piG=risoluzioneSistema(q)

        print "\nLa distribuzione di prob dei vari stati risulta essere: \n",piG,"\ndi lunghezza:",len(piG),"con somma di:",sum(piG),"\n"

        # Settaggio delle varie P(k,n) per le diverse stazioni al variare del num. persone nel sistema
        preparazioneCalcoloIndici(md,piG,n)


    # Calcolo degli indici veri e propri
    calcoloIndici(md)


