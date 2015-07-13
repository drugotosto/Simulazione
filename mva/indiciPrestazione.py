__author__ = 'maury'

import numpy as np
import struttureDati.gestoreModello as gsm

def calcoloIndiciPrestazione(md,dim):
    n=dim
    nMedio=np.zeros((dim+1,4))
    xMedio=np.zeros((dim+1,4))
    wMedio=np.zeros((dim+1,4))
    uMedio=np.zeros((dim+1,4))
    rMedio=np.zeros((dim+1,4))

    ricorsioneN(n,md,dim,xMedio,nMedio,wMedio,uMedio,rMedio)

    # Salvataggio dei vari indici di prestazione per le diverse stazioni all'interno del modello
    md.salvaIndici(nMedio,xMedio,wMedio,uMedio,rMedio)

    # Funzione di test per verifica indici
    test(md,dim)


def ricorsioneN(n,md,dim,xMedio,nMedio,wMedio,uMedio,rMedio):
    # Caso base
    if n==0:
        # Ciclo su tutte le stazioni per il calcolo
        for j in range(len(md.stazioni)):
            nMedio[n][j]=0.0
    # Caso con N>=1
    else:
        ricorsioneN(n-1,md,dim,xMedio,nMedio,wMedio,uMedio,rMedio)
        # Iterazione su tutte le stazioni per il calcolo dei vari W
        for j in range(len(md.stazioni)):
            # Differenzio per il calocolo delle W
            if md.stazioni[j].tipo == "server":
                wMedio[n][j]=md.stazioni[j].s*(1.0+nMedio[n-1][j])
            else:
                wMedio[n][j]=md.stazioni[j].s

        # Calcolo di Xo
        x0=float(n)/calcoloTempoCiclo(n,md,wMedio,rMedio)

        # Iterazione su tutte le stazioni per il calcolo dei vari X,U,N
        for j in range(len(md.stazioni)):
            xMedio[n][j]=md.stazioni[j].visite*x0
            uMedio[n][j]=xMedio[n][j]*md.stazioni[j].s
            if md.stazioni[j].tipo == "server":
                nMedio[n][j]=uMedio[n][j]*(1.0+nMedio[n-1][j])
            else:
                nMedio[n][j]=xMedio[n][j]*md.stazioni[j].s


def calcoloTempoCiclo(n,md,wMedio,rMedio):
    tot=0.0
    for i in range(len(md.stazioni)):
        if md.stazioni[i].tipo == "server":
            tot+=md.stazioni[i].visite*wMedio[n][i]
        else:
            tot+=md.stazioni[i].visite*md.stazioni[i].s
    # Calcolo Tempo di risposta per le varie stazioni
    for i in range(len(md.stazioni)):
        rMedio[n][i]=tot-(md.stazioni[0].s*md.stazioni[0].visite+md.stazioni[3].s*md.stazioni[3].visite)
        if md.stazioni[i].tipo == "server":
                rMedio[n][i]-=md.stazioni[i].s*md.stazioni[i].visite
    return tot


def test(md,dim):
    # Calcolo delle prob del #persone alle varie stazioni
    calcoloProb(md,dim)

    # Verifia che le righe delle varie prob delle stazioni sommano a 1
    # print "Somma :",[map(sum,md.stazioni[i].prob) for i in range(4)]

    # Calcolo #Medio persone per stazione
    #   numMedioPersone(md,dim)

    # Somma per colonne del #Medio di persone su ogni stazione
    lista=[]
    for j in range(dim+1):
        som=0.0
        for i in range(len(md.stazioni)):
            som+=md.stazioni[i].indici['N'][j]
        lista.append(som)

    # print("Somma N:",lista)

    # Stampa dei valori degi vari indici per tutte le stazioni
    listaIndici=gsm.ritornaIndice(md,'N')
    for i in range(len(md.stazioni)):
        print "La lista di indici N per la stazione ",i,": ",listaIndici[i]


def calcoloProb(md,dim):
    # Ciclo sulle varie stazioni...
    for i in range(len(md.stazioni)):
        # Ciclo sulle righe delle prob di ogni stazione..
        for j in range(dim):
            # Ciclo sulle colonne di ogni stazione partendo dal "fondo"
            z=j
            while(z>0):
                # Tutte le prob che non siano quelle della prima colonna
                if((z!=0) and (z<=j)):
                    # Differenzio calcolo nel caso sia load dep. o meno
                    if(md.stazioni[i].tipo=="infinite"):
                        md.stazioni[i].prob[j][z]=md.stazioni[i].prob[j-1][z-1]*md.stazioni[i].indici['X'][j]*(md.stazioni[i].s/j)
                    else:
                        md.stazioni[i].prob[j][z]=md.stazioni[i].prob[j-1][z-1]*md.stazioni[i].indici['X'][j]*md.stazioni[i].s
                z-=1
            # Caso speciale 1elemento
            if(j==0 and z==0):
                md.stazioni[i].prob[j][z]=1.0
            # Caso in cui si deve riempire la prima colonna
            elif (j>0 and z==0):
                y=1
                som=0.0
                while (y<=j):
                    som+=md.stazioni[i].prob[j][y]
                    y+=1
                md.stazioni[i].prob[j][z]=1.0-som

def numMedioPersone(md,dim):
    # Ciclo sulle varie stazioni...
    for i in range(len(md.stazioni)):
        # Calcolo la prob al variare delle persone nel sistema partendo da 1
        for j in range(1,dim):
            k=1
            som=0.0
            while (k<=j):
                if(md.stazioni[i].tipo=="infinite"):
                    som+=k*md.stazioni[i].indici['X'][j]*(md.stazioni[i].s/j)*md.stazioni[i].prob[j-1][k-1]
                else:
                    som+=k*md.stazioni[i].indici['X'][j]*md.stazioni[i].s*md.stazioni[i].prob[j-1][k-1]
                k+=1
            md.stazioni[i].indici['N'][j]=som
