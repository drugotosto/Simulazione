__author__ = 'maury'

"""
    Classe che mi rappresenta le stazioni di tipo Erlang_k (sottoclasse della classe Stazione)
    - k: parametro della distribuzione Erlang associata alla stazione
"""
from stazione import Stazione

class StazioneErlang(Stazione):
    def __init__(self,stazione,n):
        Stazione.__init__(self,stazione,n)
        self.k=stazione["k"]


