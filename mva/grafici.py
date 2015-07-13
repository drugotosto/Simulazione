__author__ = 'maury'

from settaggi import *
import numpy as np
import matplotlib.pyplot as plt

# Creazione grafici dei vari indici per le varie stazioni
def graficiIndice(indici):
    x=np.arange(n+1)
    y0=indici[0]
    y1=indici[1]
    y2=indici[2]
    y3=indici[3]

    plt.title("Persone")
    plt.xlabel("#Utenti")
    plt.ylabel("# medie Persone")
    plt.plot(x,y0,"k",x,y1,"b",x,y2,"g",x,y3,"y")

    """plt.title("Stazione 2")
    x=np.arange(dim)
    y=indici[2]
    y1=np.zeros(dim)
    y1+=somDomande
    # Dalla somma delle domande non considero sia la stazione dei terminali che quella di riposo
    y1=y1-(md.stazioni[0].s*md.stazioni[0].visite+md.stazioni[3].s*md.stazioni[3].visite+md.stazioni[2].s*md.stazioni[2].visite)
    # Non considero sia la stazione dei terminali che quella di riposo
    y2=dMax*x-(md.stazioni[0].s*md.stazioni[0].visite+md.stazioni[3].s*md.stazioni[3].visite+md.stazioni[2].s*md.stazioni[2].visite)

    plt.xlabel("#Utenti")
    plt.ylabel("Tempo di risposta")
    plt.plot(x,y,"b",x,y1,"r",x,y2,"r")"""

    plt.show()
