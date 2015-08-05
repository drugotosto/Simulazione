__author__ = 'maury'

"""
    Gestore per le diverse operazioni sulle diverse code (delle stazioni)
    e delle liste del Simulatore (eventList,freeList) piu scelta a caso
    della route
"""

import random as ran
import numpy as np
import bisect as bi
from struttureDati.stazione import Stazione
from struttureDati.evento import Evento

def schedula(evList,ev):
    """
    Inserisce un evento nella Future Event List in ordine
    :param evList: Future Event List associata al simulatore
    :type evList: list
    :param ev: Evento da inserire in maniera ordinata
    :type ev: Evento
    """
    ind=bi.bisect(evList,ev)
    evList.insert(ind,ev)

def accoda(staz,ev):
    """
    Inserisce un evento al fondo della coda della stazione
    :param staz: Stazione sulla cui coda andare ad inserire l'evento passato
    :type staz: Stazione
    :param ev: Evento da inserire in coda
    :type ev: Evento
    """
    staz.coda.append(ev)

def restituisci(freeList,ev):
    """
    Inserisce un evento appena gestito nella freeList
    :param freeList: Lista che contiene gli eventi gia presi in considerazione da "riclicare"
    :type freeList: list
    :param ev: Evento da inserire
    """
    freeList.append(ev)

def recProxEvento(evList):
    """
    Preleva l'evento successivo dall Future Event List
    :param evList: Future Event List (trattata come stack)
    :type evList: list
    :return: Evento successivo da prendere in considerazione (primo evento della lista)
    """
    return evList.pop(0)

def deQueueEvent(staz):
    """
    Preleva prossimo evento (job) dalla coda della stazione
    :param staz: Stazione da cui andare a recuperare l'evento
    :type staz: Stazione
    :return: Evento da restituire
    """
    return staz.coda.pop(0)

def chooseRoute(arr):
    """
    Ritorna una strada scelta a caso tra quelle possibili da percorre a partite
    dalla stazione da cui si esce
    :param arr: Lista delle diverse probabilita relative alle possibili strade da percorre
    :type arr: list
    :return: Indice della stazione su cui andare l'evento in questione finira
    """
    mTrans=np.array(arr)
    cum={}
    old=0.0
    while len(cum)<len(mTrans):
        cum[old+mTrans.max()]=np.argmax(mTrans)
        old=old+mTrans.max()
        mTrans.itemset(np.argmax(mTrans),0.0)
    ran.seed()
    n=ran.random()
    # print "Valore casuale",n,"valore tornato:",find_ge(sorted(cum.keys()),n),"verso stazione:",cum[find_ge(sorted(cum.keys()),n)]
    return cum[find_ge(sorted(cum.keys()),n)]

# Metodo di ricerca veloce di un valore all'interno di un array ordinato
def find_ge(a,x):
    """
    Funzione che attraverso un algoritmo di bisezione della libreria garantisce l'inserimento
    effeciente di un oggetto all'interno di una lista gia ordinata
    :param a: Lista gia ordinata
    :param x: Oggetto da inserire
    """
    'Find leftmost item greater than or equal to x'
    i = bi.bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError