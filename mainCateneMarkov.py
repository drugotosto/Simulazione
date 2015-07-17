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

    for n in range(0,n):
        # Generazione dello spazio degli stati
        spazio=generaSpazioStati(n)

        """if (11,0,2,2) in spazio:
            print "Presente"
        else:
            print "Assente"
        print "spazio:",spazio,"\nnumero:",len(spazio)"""

        # Dizionario con indice numerico 0,1,2,... con valori tuple formate da: ((n,n,n,n),'(n,n,n,n),'xi')
        spazioStati={i:(stat,str(stat)) for i,stat in enumerate(spazio)}

          # Aggiunta dello spazio degli stati al modello
        gsm.aggiungiSpazio(md,spazioStati,n)

        print "Spazio deglis stati:",md.spazioStati
        print "Lunghezza Spazio degli stati: ",len(md.spazioStati)

        # Chiamata per la creazione della matrice Q
        q=creazioneMatriceQ(md)

        print "\nLA MATRICE Q risulta essere:",q

        # Chiamata per la risoluzione del sistema
        piG=risoluzioneSistema(q)

        print "La distribuzione di prob dei vari stati risulta essere: \n",piG,"\ndi lunghezza:",len(piG),"con somma di:",sum(piG)

        # Settaggio delle varie P(k,n) per le diverse stazioni al variare del num. persone nel sistema
        # settaggioProbStaz(md,piG,n)



