__author__ = 'maury'

"""
    Gestore degli eventi per le diverse operazioni sulle diverse code (coda) delle stazioni
    e liste del Simulatore (eventList,freeList)
"""

import random as ran
import numpy as np
import bisect as bi

# Inserisce un evento nella Future Event List in ordine
def schedula(evList,ev):
    pass

# Inserisce un evento al fondo della coda della stazione
def accoda(staz,ev):
    pass

# Inserisce un evento appena gestito nella freeList
def restituisci(freeList,ev):
    pass

# Preleva un evento dall Future Event List
def recProxEvento(evList):
    pass

# Preleva prossimo job dalla coda della stazione
def deQueueEvent(staz):
    pass

# Ritorna una strada scelta a caso tra quelle possibili da percorre a partite dalla stazione da cui si esce
def chooseRoute(arr):
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
    'Find leftmost item greater than or equal to x'
    i = bi.bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError