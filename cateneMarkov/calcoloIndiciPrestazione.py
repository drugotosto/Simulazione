__author__ = 'maury'
import numpy as np
from settaggi import m


def calcoloIndiciPrest(md,piG,n):
    # Calcolo delle varie P(k,n) e ritorna la corrispondente matrice
    matPk=settaggioProbStaz(md,piG,n+1)

    # Salvataggio nel modello delle varie distribuzioni per le varie stazioni al variare del n_persone
    for i in range(len(matPk)):
        md.stazioni[i].prob[n]=matPk[i]

    # Stampa...
    for i in range(len(matPk)):
        print "Stazione",i,"************"
        for val in md.stazioni[i].prob.items():
            print "Con N:",val[0],"persone dentro avremo P:",val[1]

    # Calcolo degli indici veri e propri
    calcoloIndici(md)

# Calcolo delle varie P(k,n) per le diverse stazioni dato la distr. di prob. per un dato valore di n
def settaggioProbStaz(md,piG,dim):

    # Matrice di prob per ogni stazione di dimensione "n+1" (0,1,...n) che conterra i vari P(k,n) da k=0...n
    matPk=np.zeros((m,dim))

    for i,p in enumerate(piG):
        print "Valore di prob:",p,"corrispondente allo stato:",md.spazioStati[i][0]
        # Per ogni stato ciclo sulle diverse posizioni/stazioni esaminando il n_persone al suo interno
        for j,val in enumerate(md.spazioStati[i][0]):
            if val!=0:
                matPk[j][val]=+p

    # Settaggio elementi P[i][0] per ogni stazione
    for i in range(len(matPk)):
        matPk[i][0]=1.0-sum(matPk[i])

    return matPk



def calcoloIndici(md):
    print "\n------INDICI DI PRESTAZIONE-------"