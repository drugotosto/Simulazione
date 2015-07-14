__author__ = 'maury'
import itertools
import numpy as np
from settaggi import *

#
def generaSpazioStati():
    # Prodotto Cartesiano di tutti i possibili elementi dati dall'array (0,1,2,3,...15)
    comb=list(itertools.product(range(0,n+1), repeat=m))
    # Si sottraggono poi tutti questi elementi la cui somma non arriva ad un totale di n
    comb=[val for val in comb if sum(val)==n]
    return comb

# Metodo per la creazione della matrice Q
def creazioneMatriceQ(md):
    q=np.zeros((len(md.spazioStati),len(md.spazioStati)))

    """Ciclo sullo spazio degli stati e per ogni stato:
        - Considero i valori per ogni posizione !=0 vado a vedere sulla matrice P tutti le colonne della
          corrispondente riga che hanno valore !=0 capendo così su quale stato ci si riesce a spostare...
        - Effettuo la conversione dei vari stati trovati al passo precedente recuperando l'indice della
          colonna della Q su cui andare ad inserire il corrispondente valore calcolato a parte
        - Eseguo la trasposta della matrice Q per passare da piGreco*Q=0 -> Q*piGreco=0 e setto la
          condizione iniziale"""

    # Metodo per riuscire a trovare l'indice relativo alla colonna della matrice Q su cui poi andare a settare il giusto valore
    indice=[key for key,value in md.spazioStati.iteritems() if value[0]==(4,0,0,0)]

    print "chiave:",indice[0],"tipo:",type(indice[0])

    return q


