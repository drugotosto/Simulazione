__author__ = 'maury'

"""
    Gestore per le diverse operazioni sulle diverse code (delle stazioni)
    e delle liste del Simulatore (eventList,freeList) piu scelta a caso
    della route
"""

import random as ran
import collections
import numpy as np
import bisect as bi
import copy
from struttureDati.stazione import Stazione
from struttureDati.evento import Evento
from simulatore import *

def schedula(evList,ev):
    """
    Inserisce un evento nella Future Event List in ordine
    :param evList: Future Event List associata al simulazione
    :type evList: list
    :param ev: Evento da inserire in maniera ordinata
    :type ev: Evento
    """
    ind=bi.bisect(evList,ev)
    evList.insert(ind,ev)

def recProxEvento(evList):
    """
    Preleva l'evento successivo dall Future Event List
    :param evList: Future Event List (trattata come stack)
    :type evList: list
    :return: Evento successivo da prendere in considerazione (primo evento della lista)
    """
    return evList.pop(0)

def accoda(staz,ev):
    """
    Inserisce un evento al fondo della coda della stazione
    :param staz: Stazione sulla cui coda andare ad inserire l'evento passato
    :type staz: Stazione
    :param ev: Evento da inserire in coda
    :type ev: Evento
    """
    staz.coda.append(ev)

def deQueueEvent(staz):
    """
    Preleva prossimo evento (job) dalla coda della stazione
    :param staz: Stazione da cui andare a recuperare l'evento
    :type staz: Stazione
    :return: Evento da restituire
    """
    return staz.coda.pop(0)

def restituisci(freeList,ev):
    """
    Inserisce un evento appena gestito nella freeList
    :param freeList: Lista che contiene gli eventi gia presi in considerazione da "riclicare"
    :type freeList: list
    :param ev: Evento da inserire
    """
    freeList.append(ev)

def chooseRoute(arr,route):
    """
    Ritorna una strada scelta a caso tra quelle possibili da percorre a partite
    dalla stazione da cui si esce
    :param arr: Lista delle diverse probabilita relative alle possibili strade da percorre
    :type arr: list
    :return: Indice della stazione su cui l'evento in questione finira
    """
    num=route.random()
    mTrans=np.array(arr)
    cum={}
    old=0.0
    while len(cum)<len(mTrans):
        cum[old+mTrans.max()]=np.argmax(mTrans)
        old=old+mTrans.max()
        mTrans.itemset(np.argmax(mTrans),0.0)
    # print "DIZ:",cum
    ind=ricerca(num,sorted(cum.keys()))
    # print "LISTA ORD:",sorted(cum.keys())
    # print "Valore casuale",num,"verso stazione:",cum[ind]
    return cum[ind]

# Metodo di ricerca di un valore all'interno di un array ordinato
def ricerca(n,lista):
    for i,val in enumerate(lista):
        if val>=n:
            return val

def stampaSituazione(sim,clock):
    """
    Stampa a video della situazione del Simulatore con rispettiva Future Event List
    e code delle varie stazioni
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    """
    print "\n\n!!!!!!!!!!!!! CLOCK:",clock," !!!!!!!!!!!!"
    # Stampa della Future Event List
    print "\n-----EVENT LIST-----"
    for event in sim.eventList:
        print "Evento:",vars(event)

    # Stampa delle code delle stazioni
    print "\n+++++CODE STAZIONI+++++"
    for staz in sim.md.stazioni:
        print "Stazione",staz.id
        for ev in staz.coda:
            print "evento:",vars(ev)


def calcoloStampaIndici(sim):
    """
    Calcolo e stampa a video degli indici di prestazione per le diverse stazioni
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    """
    for staz in sim.md.stazioni:
        print "\nStazione:",staz.id,"nome:",staz.nome
        staz.indici["U"]=staz.busyT/sim.time
        print "UTILIZZAZIONE:",staz.indici["U"]
        staz.indici["X"]=staz.partenze/sim.time
        print "THROUGHPUT:",staz.indici["X"]
        if staz.partenze!=0:
            staz.indici["W"]=staz.area/staz.partenze
        print "T. MEDIO PERMANENZA:",staz.indici["W"]
        staz.indici["N"]=staz.area/sim.time
        print "N. MEDIO PERSONE:",staz.indici["N"],"\n"

    for i,staz in enumerate(sim.md.stazioni):
        print "Visite alla stazione",i,"sono:",staz.partenze

    print "\nTEMPO CICLO Stazione 0 job 1 utilizzando \"time stamp\":",sim.md.stazioni[0].tCicloJob

def controlloFine(sim,ev,nj,indStaz):
    """
    Controllo che sia in una situazione di E.O
    :param sim: Oggetto simulatore
    :type sim: Simulatore
    :param ev: Prox evento da gestire
    :type ev: Evento
    :param nj: Numero di eventi in coda alla stazione 0 (come ero partito)
    :return: True sono in E.O. False altrimenti
    """
    if sim.md.stazioni[indStaz].tipo!="infinite":
        if sim.md.stazioni[indStaz].Njobs==nj+1 and len(sim.md.stazioni[indStaz].coda)==nj and ev.tipo=="partenza" and ev.idStaz==indStaz:
            return True
        else:
            return False
    else:
        if sim.md.stazioni[indStaz].Njobs==nj+1 and ev.idStaz==indStaz and ev.tipo=="partenza":
            return True


