__author__ = 'maury'

"""
    Gestore del modello analitico che mette a disposizione funzioni utili alla gestione e all'analisi del
    modello che si reupera come parametro delle funzioni stesse
"""

import json

from struttureDati.modello import *


def caricamentoModello(path,dim):
    with open(path) as file:
        model = json.loads(file.read())
        return Modello(model["stazioni"],model["q"],dim)

def stampaStazioni(md):
    for staz in  md.stazioni:
        print "Stazione ",staz.id,": ",vars(staz)

# Ritorna un dizionario di liste ognuna in riferimento ad una stazione per il tipo di indice scelto
def ritornaIndice(md,indice):
    return {i:md.stazioni[i].indici[indice] for i in range(4)}

# Ritorna una lista di valori in merito all'indice scelto e per la data stazione scelta
def ritornaIndiceStazione(md,indice,indStazione):
    return md.stazioni[indStazione].indici[indice]



