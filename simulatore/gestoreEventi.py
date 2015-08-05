from struttureDati.distStazione import genDistrMisura

__author__ = 'maury'

"""
    Gestore degli eventi che fanno parte della Future Event List
"""

from tools import *

def arrivo(sim):
    return True

def partenza(sim):
    return True

def misura(sim):
    """
    Gestione dell'evento di misura con conseguente stampa indici e
    rischedulazione dello stesso evento
    :param sim:
    :return:
    """
    schedula(sim.eventList,Evento(sim.time,-1,genDistrMisura(sim.time),"misura",-1,-1))
    return True

def fine(sim):
    return False
