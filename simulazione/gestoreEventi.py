__author__ = 'maury'

"""
    Gestore degli eventi che fanno parte della Future Event List
"""

from tools import *
from classTools import Display
from struttureDati.distStazione import genTempMisura
from struttureDati.evento import Evento

def arrivo(sim,event):
    """
    Gestione di un arrivo ad una stazione
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    print "\nARRIVO del job:",event.idJob,"dalla stazione:",event.idStaz
    sim.md.stazioni[event.idStaz].arrivi+=1
    sim.md.stazioni[event.idStaz].Njobs+=1
    servT=sim.listDistrStaz[event.idStaz].genDistr()
    partT=servT+sim.time
    print "NUM JOBS alla stazione",event.idStaz,"sono:",sim.md.stazioni[event.idStaz].Njobs
    # Un solo evento alla stazione
    if sim.md.stazioni[event.idStaz].Njobs==1:
        # Schedulo partenza dello stesso evento da questa stazione nel caso prelevando dalla freeList
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
            schedula(sim.eventList,freeEv)
            print "Schedulato Evento nella Future Event List:",vars(freeEv)
        else:
            nextEv=Evento(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
            schedula(sim.eventList,nextEv)
            print "Schedulato Evento nella Future Event List:",vars(nextEv)
    # Accodo l'evento alla stazione
    else:
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,servT,-1,"coda",event.idJob,event.idStaz)
            accoda(sim.md.stazioni[event.idStaz],freeEv)
            print "Accodato evento alla stazione:",vars(freeEv)
        else:
            nextEv=Evento(sim.time,servT,-1,"coda",event.idJob,event.idStaz)
            accoda(sim.md.stazioni[event.idStaz],nextEv)
            print "Accodato evento alla stazione:",vars(nextEv)
    return True

def partenza(sim,event):
    """
    Gestione di una partenza da una stazione
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    print "\nPARTENZA del job:",event.idJob,"dalla stazione:",event.idStaz
    sim.md.stazioni[event.idStaz].partenze+=1
    sim.md.stazioni[event.idStaz].Njobs-=1
    print "NUM JOBS alla stazione",event.idStaz,"sono:",sim.md.stazioni[event.idStaz].Njobs
    # Nel caso ci fossero piu eventi in stazione
    if sim.md.stazioni[event.idStaz].Njobs>=1:
        ev=deQueueEvent(sim.md.stazioni[event.idStaz])
        """:type : Evento"""
        partT=sim.time+ev.serT
        # Schedulo partenza del prossimo evento da questa stazione nel caso prelevando dalla freeList
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,ev.serT,partT,"partenza",ev.idJob,ev.idStaz)
            schedula(sim.eventList,freeEv)
            print "Schedulato Evento dalla coda:",vars(freeEv)
        else:
            nextEv=Evento(sim.time,ev.serT,partT,"partenza",ev.idJob,ev.idStaz)
            schedula(sim.eventList,nextEv)
            print "Schedulato Evento dalla coda:",vars(nextEv)
    # Schedulo un arrivo alla stazione successiva (se esistono piu strade ne scelgo una a caso)
    print "\nProbabilita di transizione dalla stazione:",event.idStaz,"sono:",sim.md.q[event.idStaz]
    # Controllo che ci sia la possibilita di prendere strade differenti
    if sim.md.q[event.idStaz].count(0.0)<(len(sim.md.stazioni)-1):
        indNextStaz=chooseRoute(sim.md.q[event.idStaz])
    else:
        indNextStaz=sim.md.q[event.idStaz].index(1.0)
    # Schedulo arrivo di questo stesso evento alla prox stazione
    if len(sim.freeList)>0:
        freeEv=sim.freeList.pop()
        """:type : Evento"""
        freeEv.settaggioValori(sim.time,-1,sim.time,"arrivo",event.idJob,indNextStaz)
        schedula(sim.eventList,freeEv)
        print "Schedulato Evento nella Future Event List:",vars(freeEv)
    else:
        nextEv=Evento(sim.time,-1,sim.time,"arrivo",event.idJob,indNextStaz)
        schedula(sim.eventList,nextEv)
        print "Schedulato Evento nella Future Event List:",vars(nextEv)
    return True

def misura(sim,event):
    """
    Gestione dell'evento di misura con conseguente stampa indici
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    print "\nINDICI PRESTAZIONE"
    # Calcolo dei vari indici di prestazione e relativa stampa

    # Se la freeList del simulazione contine almeno un evento gia elaborato allora esso viene "riciclato"
    if len(sim.freeList)>0:
        freeEv=sim.freeList.pop()
        """:type : Evento"""
        freeEv.settaggioValori(sim.time,-1,genTempMisura(sim.time),"misura",-1,-1)
        schedula(sim.eventList,freeEv)
    else:
        nextEv=Evento(sim.time,-1,genTempMisura(sim.time),"misura",-1,-1)
        schedula(sim.eventList,nextEv)
    return True

def fine(sim,event):
    """
    Gestione della fine simulazione
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :return: Fine simulazione
    """
    return False
