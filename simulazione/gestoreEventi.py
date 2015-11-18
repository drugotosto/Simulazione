__author__ = 'maury'

"""
    Gestore degli eventi che fanno parte della Future Event List
"""

from tools import *
from classTools import Display
from struttureDati.servizio import genTempMisura
from struttureDati.evento import Evento

def arrivo(sim,event,okStop,route):
    """
    Gestione di un arrivo ad una stazione.
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    # print "\nGESTISCO ARRIVO: ",vars(event)
    sim.md.stazioni[event.idStaz].arrivi+=1
    sim.md.stazioni[event.idStaz].Njobs+=1
    # Genero una istanza della distribuzione del tempo di servizio associata alla stazione di arrivo
    servT=sim.md.stazioni[event.idStaz].genTempSer()
    partT=servT+sim.time
    # print "NUM JOBS alla stazione",sim.md.stazioni[event.idStaz].id,"sono:",sim.md.stazioni[event.idStaz].Njobs
    # print "Tempo di servizio:",servT
    # La stazione non e I.S.
    if sim.md.stazioni[event.idStaz].tipo!="infinite":
        # Un solo evento alla stazione
        if sim.md.stazioni[event.idStaz].Njobs==1 and len(sim.md.stazioni[event.idStaz].coda)==0:
            # Schedulo partenza dello stesso evento da questa stazione nel caso prelevando dalla freeList se ci sono eventi passati
            if len(sim.freeList)>0:
                freeEv=sim.freeList.pop()
                """:type : Evento"""
                freeEv.settaggioValori(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
                schedula(sim.eventList,freeEv)
                # print "Schedulata Partenza nella Future Event List:",vars(freeEv),"perche il job era unico in coda"
            else:
                nextEv=Evento(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
                schedula(sim.eventList,nextEv)
                # print "Schedulato Partenza nella Future Event List:",vars(nextEv),"perche il job era unico in coda"
        # Accodo l'evento alla stazione
        else:
            if len(sim.freeList)>0:
                freeEv=sim.freeList.pop()
                """:type : Evento"""
                freeEv.settaggioValori(sim.time,servT,-1,"coda",event.idJob,event.idStaz)
                accoda(sim.md.stazioni[event.idStaz],freeEv)
                # print "Accodato evento alla stazione:",vars(freeEv)
            else:
                nextEv=Evento(sim.time,servT,-1,"coda",event.idJob,event.idStaz)
                accoda(sim.md.stazioni[event.idStaz],nextEv)
                # print "Accodato evento alla stazione:",vars(nextEv)
    else:
        # Schedulo subito la partenza dello stesso evento da I.S. nel caso prelevando dalla freeList se ci sono eventi passati
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
            schedula(sim.eventList,freeEv)
            # print "Schedulata Partenza nella Future Event List:",vars(freeEv),"perche la stazione e I.S."
        else:
            nextEv=Evento(sim.time,servT,partT,"partenza",event.idJob,event.idStaz)
            schedula(sim.eventList,nextEv)
            # print "Schedulato Partenza nella Future Event List:",vars(nextEv),"perche la stazione e I.S."
    if okStop==False:
        return False
    else:
        return True

def partenza(sim,event,okStop,route):
    """
    Gestione di una partenza da una stazione
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    # print "\nGESTISCO PARTENZA: ",vars(event)
    sim.md.stazioni[event.idStaz].partenze+=1
    sim.md.stazioni[event.idStaz].Njobs-=1
    # print "NUM JOBS alla stazione:",sim.md.stazioni[event.idStaz].id,"dopo la partenza sono:",sim.md.stazioni[event.idStaz].Njobs
    # Nel caso ci fossero altri eventi in stazione e la stazione non e I.S.
    if len(sim.md.stazioni[event.idStaz].coda)>=1 and sim.md.stazioni[event.idStaz].tipo!="infinite":
        ev=deQueueEvent(sim.md.stazioni[event.idStaz])
        """:type : Evento"""
        partT=sim.time+ev.serT
        # Schedulo partenza del prossimo evento da questa stazione nel caso prelevando dalla freeList
        if len(sim.freeList)>0:
            freeEv=sim.freeList.pop()
            """:type : Evento"""
            freeEv.settaggioValori(sim.time,ev.serT,partT,"partenza",ev.idJob,ev.idStaz)
            schedula(sim.eventList,freeEv)
            # print "Schedulato Evento dalla coda:",vars(freeEv),"e inserito in Event List"
        else:
            nextEv=Evento(sim.time,ev.serT,partT,"partenza",ev.idJob,ev.idStaz)
            schedula(sim.eventList,nextEv)
            # print "Schedulato Evento dalla coda:",vars(nextEv),"e inserito in Event List"
    # Schedulo un arrivo alla stazione successiva (se esistono piu strade ne scelgo una a caso)
    # Controllo nel caso ci sia la possibilita di prendere strade differenti
    if sim.md.q[event.idStaz].count(0.0)<(len(sim.md.stazioni)-1):
        # print "Esistono piu strade percorribili..."
        indNextStaz=chooseRoute(sim.md.q[event.idStaz],route)
        # print "Prox Staz:",indNextStaz
    else:
        indNextStaz=sim.md.q[event.idStaz].index(1.0)
        # print "Prox Staz:",indNextStaz
    # Schedulo arrivo di questo stesso evento alla prox stazione
    if len(sim.freeList)>0:
        freeEv=sim.freeList.pop()
        """:type : Evento"""
        freeEv.settaggioValori(sim.time,-1,sim.time,"arrivo",event.idJob,indNextStaz)
        schedula(sim.eventList,freeEv)
        # print "Schedulato Evento \"arrivo\" nella Future Event List:",vars(freeEv)
    else:
        nextEv=Evento(sim.time,-1,sim.time,"arrivo",event.idJob,indNextStaz)
        schedula(sim.eventList,nextEv)
        # print "Schedulato Evento \"arrivo\" nella Future Event List:",vars(nextEv)
    if okStop==False:
        return False
    else:
        return True

def misura(sim,event,okStop,route):
    """
    Gestione dell'evento di misura con conseguente stampa indici
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    # print "\nINDICI PRESTAZIONE"
    # Calcolo dei vari indici di prestazione e relativa stampa
    # calcoloStampaIndici(sim)
    # Se la freeList del simulazione contine almeno un evento gia elaborato allora esso viene "riciclato"
    if len(sim.freeList)>0:
        freeEv=sim.freeList.pop()
        """:type : Evento"""
        freeEv.settaggioValori(sim.time,-1,genTempMisura(sim.time),"misura",-1,-1)
        schedula(sim.eventList,freeEv)
    else:
        nextEv=Evento(sim.time,-1,genTempMisura(sim.time),"misura",-1,-1)
        schedula(sim.eventList,nextEv)
    if okStop==False:
        return False
    else:
        return True

def fineTransizione(sim,event,okStop,route):
    """
    Gestisco la fine transizione andando a resettare tutti i valori ed indici di tutte le stazioni (
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :type event: Evento
    :return: Continua simulazione
    """
    for staz in sim.md.stazioni:
        staz.resettaCampi()
    if okStop==False:
        return False
    else:
        return True

def fine(sim,event,okStop,route):
    """
    Gestione della fine simulazione
    :param sim: Oggetto Simulatore
    :type sim: Simulatore
    :param event: Oggetto Evento da gestire
    :return: Fine simulazione
    """
    return True
