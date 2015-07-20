__author__ = 'maury'

"""
    Classe che descrive il modello analitico preso in esame formato da:
    - stazioni: lista di oggetti di tipo "stazione"
    - q: matrice delle tranzioni
    - spazioStati: spazio degli stati totale con "n" persone all'interno del sistema
    - n: numero persone totali all'interno del sistema
"""

from struttureDati.stazione import *
from struttureDati.stazioneErlang import *
from settaggi import m

class Modello():
    def __init__(self,stazioni,q,n):
        self.stazioni=[]
        # Lista di dizioniari che verra trasormata in una lista di oggetti Stazione
        for staz in stazioni:
            if(staz["tipo"]!="erlang"):
                self.stazioni.append(Stazione(staz,n))
            else:
                self.stazioni.append(StazioneErlang(staz,n))
        self.q=q

    def setSpazio(self,spazioStati,n):
        self.spazioStati=spazioStati
        self.numPersone=n

    def aggiornaVisite(self,visite):
        for staz,val in zip(self.stazioni,visite):
            staz.visite=val

    def aggiornaDomande(self,domande):
        for staz,val in zip(self.stazioni,domande):
            staz.domande=val

    def ritornaSommaDomande(self):
        sumD=0.0
        for staz in self.stazioni:
            sumD=sumD+staz.domande
        return sumD

    def salvaIndici(self,nMedio,xMedio,wMedio,uMedio,rMedio):
        for i in range(m):
            colX=[row[i] for row in xMedio]
            colN=[row[i] for row in nMedio]
            colW=[row[i] for row in wMedio]
            colU=[row[i] for row in uMedio]
            colR=[row[i] for row in rMedio]
            self.stazioni[i].indici['X']=colX
            self.stazioni[i].indici['N']=colN
            self.stazioni[i].indici['W']=colW
            self.stazioni[i].indici['U']=colU
            self.stazioni[i].indici['R']=colR

    def salvaIndiciMark(self,nMedio,xMedio,wMedio,uMedio,rMedio):
        for i in range(m):
            self.stazioni[i].indiciMark['X']=xMedio[i]
            self.stazioni[i].indiciMark['N']=nMedio[i]
            self.stazioni[i].indiciMark['W']=wMedio[i]
            self.stazioni[i].indiciMark['U']=uMedio[i]
            self.stazioni[i].indiciMark['R']=rMedio[i]

