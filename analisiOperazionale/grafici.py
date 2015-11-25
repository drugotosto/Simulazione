__author__ = 'maury'

import numpy as np
import matplotlib.pyplot as plt

# Creazione grafico dell' asintoto orizzontale e obliquo per X
def graficoAsintotico(dMax,som_domande,md):
    x=np.arange(0,100)
    y1=np.zeros(100)
    y1+=1/dMax
    y2=(1/(som_domande))*x
    p1x,p1y=genPuntiInt(dMax,som_domande)
    plt.subplot(211)

    plt.title("ANALISI ASINTOTICA")
    plt.ylabel("Throughput")
    plt.plot(x,y1,"r",x,y2,"g")
    plt.annotate("Inizio code",xy=(p1x,p1y),xytext=(p1x+1,p1y+0.5),arrowprops=dict(facecolor='black', shrink=0.05))

    plt.subplot(212)
    x=np.arange(0,100)
    y1=np.zeros(100)
    y1+=som_domande
    # Dalla somma delle domande non considero la stazione dei terminali stessa
    y1=y1-(md.stazioni[0].s*md.stazioni[0].visite)
    # Non considero la stazione dei terminali
    y2=dMax*x-(md.stazioni[0].s*md.stazioni[0].visite)
    y3=(md.stazioni[1].s*md.stazioni[1].visite)*x-(md.stazioni[0].s*md.stazioni[0].visite)

    plt.xlabel("#Utenti")
    plt.ylabel("Tempo di risposta")
    plt.plot(x,y1,"r",x,y2,"g",x,y3,"b--")
    plt.show()
    return p1x

# Genera il punto di interdecazione tra i due asintoti (#jobs dopo il quale si formano le code)
def genPuntiInt(dMax,som_domande):
    m=np.array(((1/som_domande,-1),(0,1)))
    c=np.array((0,1/dMax))
    x1, y1 = np.linalg.solve(m,c)
    return x1,y1