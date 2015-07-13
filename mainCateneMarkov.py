__author__ = 'maury'

"""
    MAIN PRINCIPALE
"""
from settaggi import *
from struttureDati import gestoreModello as gsm
from analisiOperazionale import *
from cateneMarkov import *


if __name__=='__main__':
    print "\nCostruzione catena di MArkov del modello dato come progetto finale (modello di un sistema)\n"

    # Definzione #persone per cui si calcolano gli indici di prestazione
    dim=2

    comb=generaCombinazioni()
    print("COMBINAZIONI:",comb)
