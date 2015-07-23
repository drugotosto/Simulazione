__author__ = 'maury'
import numpy as np
from settaggi import *


def preparazioneCalcoloIndici(md,piG,dim):
    # Calcolo delle varie P(k,n) e ritorna la corrispondente matrice
    matPk=settaggioProbStaz(md,piG,dim+1)

    # Salvataggio nel modello delle varie distribuzioni per le varie stazioni al variare del n_persone
    for i in range(len(matPk)):
        md.stazioni[i].prob[dim]=matPk[i]

    # Stampa...
    for i in range(len(matPk)):
        print "Stazione",i,"************"
        for val in md.stazioni[i].prob.items():
            print "Con N:",val[0],"persone dentro avremo P:",val[1]


# Calcolo delle varie P(k,n) per le diverse stazioni dato la distr. di prob. per un dato valore di n
def settaggioProbStaz(md,piG,dim):

    # Matrice di prob per ogni stazione di dimensione "n+1" (0,1,...n) che conterra i vari P(k,n) da k=0...n
    matPk=np.zeros((m,dim))

    for i,p in enumerate(piG):
        if md.spazioStati[i].tipo!="erlang":
            print "Valore di prob:",p,"corrispondente allo stato:",md.spazioStati[i].stato
        else:
            print "Valore di prob:",p,"corrispondente allo stato:",md.spazioStati[i].stato,"listStazErl:",md.spazioStati[i].listStazErl
        # Per ogni stato ciclo sulle diverse posizioni/stazioni esaminando il n_persone al suo interno
        for j,val in enumerate(md.spazioStati[i].stato):
            if val!=0:
                matPk[j][val]+=p

    # Settaggio elementi P[i][0] per ogni stazione
    for i in range(len(matPk)):
        matPk[i][0]=1.0-sum(matPk[i])

    return matPk



def calcoloIndici(md):
    print "\n------INDICI DI PRESTAZIONE-------"

    nMedio=np.zeros((m,n+1))
    xMedio=np.zeros((m,n+1))
    wMedio=np.zeros((m,n+1))
    uMedio=np.zeros((m,n+1))
    rMedio=np.zeros((m,n+1))


    # Ciclo su tutti i valori di "n"
    for i in range(1,n+1):
        # Ciclo su tutte le stazioni
        for j in range(len(md.stazioni)):
            z=1.0
            while z<=i:
                if md.stazioni[j].tipo=="server":
                    # Calcolo X
                    xMedio[j][i]+=(1.0/md.stazioni[j].s)*md.stazioni[j].prob[i][z]
                elif md.stazioni[j].tipo=="erlang":
                    xMedio[j][i]+=(1.0/(md.stazioni[j].s/md.stazioni[j].k))*md.stazioni[j].prob[i][z]
                elif md.stazioni[j].tipo=="infinite":
                    xMedio[j][i]+=(1.0/(md.stazioni[j].s/z))*md.stazioni[j].prob[i][z]
                # Calcolo N
                nMedio[j][i]+=z*md.stazioni[j].prob[i][z]
                z+=1
            # Calcolo W
            wMedio[j][i]=nMedio[j][i]/xMedio[j][i]

        # Calcolo R
        tot=0.0
        # Ciclo su tutte le stazioni per calcolare tempo di ciclo
        for j in range(len(md.stazioni)):
            tot+=md.stazioni[j].visite*wMedio[j][i]
            # Calcolo U
            uMedio[j][i]=xMedio[j][i]*md.stazioni[j].s

        # Calcolo Tempo di risposta per le varie stazioni
        for j in range(len(md.stazioni)):
            # Per tutte le stazioni non tengo conto del proprio tempo di permanenza con "n" persone dentro
            rMedio[j][i]=tot-(wMedio[j][i]*md.stazioni[j].visite)


    # STAMPA...
    print "nMEDIO:\n",nMedio
    print "\nxMEDIO:\n",xMedio
    print "\nwMEDIO:\n",wMedio
    print "\nuMEDIO:\n",uMedio
    print "\nrMEDIO:\n",rMedio

    # Salvataggio dei vari indici di prestazione per le diverse stazioni all'interno del modello
    md.salvaIndiciMark(nMedio,xMedio,wMedio,uMedio,rMedio)
