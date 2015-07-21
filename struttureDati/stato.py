__author__ = 'maury'

"""
    Classe che mi rappresenta ogni singolo stato "semplice" della catena di MARKOV
    - stato: tupla che mi descrive lo stato specifico
    - tipo: tipologia NORMALE
"""

class Stato():
    def __init__(self,stato,tipo="normale"):
        self.stato=stato
        self.tipo=tipo


