__author__ = 'maury'

"""
    Classe che descrive il modello analitico preso in esame formato da:
    - stazioni: lista di oggetti di tipo "stazione"
    - q: matrice delle tranzioni
"""

from struttureDati.stazione import *

class Modello():
    def __init__(self,stazioni,q,dim):
        self.stazioni=[]
        # Lista di dizioniari che verra trasormata in una lista di oggetti Stazione
        for staz in stazioni:
            self.stazioni.append(Stazione(staz,dim))
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
        for i in range(4):
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


