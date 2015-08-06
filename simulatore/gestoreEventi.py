__author__ = 'maury'

"""
    Gestore degli eventi che fanno parte della Future Event List
"""

from tools import *
from struttureDati.distStazione import genTempMisura
from simulatore import Simulatore
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
    sim.md.stazioni[event.idStaz].arrivi+=1
    sim.md.stazioni[event.idStaz].Njobs+=1
    servT=sim.listDistrStaz[event.idStaz].genDistr()
    partT=servT+sim.time
    # Un solo evento alla stazione
    if sim.md.stazioni[event.idStaz].Njobs==1:
        # Schedulo partenza dello stesso evento da questa stazione nel caso prelevando dalla freeList
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
            schedula(sim.eventList,freeEv)
        else:
            schedula(sim.eventList,Evento(sim.time,servT,partT,"partenza",event.idJob,event.idStaz))
    # Accodo l'evento alla stazione
    else:
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
            accoda(sim.md.stazioni[event.idStaz],freeEv)
        else:
            accoda(sim.md.stazioni[event.idStaz],Evento(sim.time,servT,-1,"coda",event.idJob,event.idStaz))
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
    sim.md.stazioni[event.idStaz].partenze+=1
    sim.md.stazioni[event.idStaz].Njobs-=1
    # Nel caso ci fossero piu eventi in stazione
    if sim.md.stazioni[event.idStaz].Njobs>1:
        ev=deQueueEvent(sim.md.stazioni[event.idStaz].coda)
        """:type : Evento"""
        partT=sim.time+ev.serT
        # Schedulo partenza del prossimo evento da questa stazione nel caso prelevando dalla freeList
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,ev.serT,partT,"partenza",ev.idJob,ev.idStaz)
            schedula(sim.eventList,freeEv)
        else:
            schedula(sim.eventList,Evento(sim.time,ev.serT,partT,"partenza",ev.idJob,ev.idStaz))
    # Schedulo un arrivo alla stazione successiva (se esistono piu strade ne scelgo una a caso)
    print "\nProbabilita di transizione dalla stazione:",event.idStaz,"sono:",sim.md.q[event.idStaz]
    indNextStaz=chooseRoute(sim.md.q[event.idStaz])
    # Schedulo arrivo di questo stesso evento alla prox stazione
    if len(sim.freeList)>0:
        freeEv=sim.freeList.pop()
        """:type : Evento"""
        freeEv.settaggioValori(sim.time,-1,sim.time,"arrivo",event.idJob,indNextStaz)
        schedula(sim.eventList,freeEv)
    else:
        schedula(sim.eventList,Evento(sim.time,-1,sim.time,"arrivo",event.idJob,indNextStaz))
    return True

def misura(sim,event):
    """
    Gestione dell'evento di misura con conseguente stampa indici
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :return: Continua simulazione
    """
    # Stampa dei vari indici di prestazione

    # Se la freeList del simulatore contine almeno un evento gia elaborato allora esso viene "riciclato"
    if len(sim.freeList)>0:
        ev=sim.freeList.pop()
        """:type : Evento"""
        ev.settaggioValori(sim.time,-1,genTempMisura(sim.time),"misura",-1,-1)
    else:
        schedula(sim.eventList,Evento(sim.time,-1,genTempMisura(sim.time),"misura",-1,-1))
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
