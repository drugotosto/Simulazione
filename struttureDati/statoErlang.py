__author__ = 'maury'

"""
    Classe che mi rappresenta ogni singolo stato "ERLANG" della catena di MARKOV
    - stato: tupla che mi descrive lo stato specifico di base
    - tipo: tipologia ERLANG
    - listaStazErl: lista di dizionari avente la coppia:
        * indStaz: indice della stazione che ha un numero di persone all'interno >0
        * stadK: stadio di servizio attivo all'interno della suddeta stazione
"""

from stato import Stato

class StatoErlang(Stato):
    def __init__(self,stato,staz=[],valK=[]):
        Stato.__init__(self,stato,'erlang')
        self.listStazErl=[{'indStaz':k,'stadK':v} for (k,v) in zip(staz,valK)]
