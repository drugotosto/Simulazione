__author__ = 'maury'

import numpy as np

class Transitorio():
    def __init__(self):
        self.numProve=0
        self.indOss=0
        self.listaOss=[]
        self.varianzeX=[]
        self.varianzeN=[]
        self.varianzeW=[]

    def calcolaMediaVarianza(self):
        """
        Vado a calcolare medie e varianze campionarie sui vari indici (delle diverse stazioni)
        in base alle diverse prove fatte per ogni osservazione rilevata.
        :return:
        """
        """print "\n\nSTAMPA delle varie prove per le diverse osservazioni!"
        for j,oss in enumerate(self.listaOss):
            print "\nPer osservazione",j,":"
            for i,prova in enumerate(oss.indiciProve):
                    print "Per la prova",i,"abbiamo valori:"
                    for k,indici in enumerate(prova.indiciStazioni):
                        print "Perl la stazione",k,"abbiamo valori:",indici"""

        # Memorizzo la somma complessiva dei vari indici (X,N), di ogni stazione, per le varie osservazioni
        for oss in self.listaOss:
            for prova in oss.indiciProve:
                for j,indStaz in enumerate(prova.indiciStazioni):
                        oss.sommeIndici[j]["SommaX"]+=indStaz["X"]
                        oss.sommeIndici[j]["SommaN"]+=indStaz["N"]
                        oss.sommeIndici[j]["SommaW"]+=indStaz["W"]

        # Calcolo delle medie degli indici (X,N) di ogni stazione rispetto alle varie osservazioni fatte
        for oss in self.listaOss:
            for j,somma in enumerate(oss.sommeIndici):
                oss.medieIndici[j]["MediaX"]=somma["SommaX"]/self.numProve
                oss.medieIndici[j]["MediaN"]=somma["SommaN"]/self.numProve
                oss.medieIndici[j]["MediaW"]=somma["SommaW"]/self.numProve

        # Calcolo della Varianza di ogni indice (X,N) per ogni stazione rispetto alle varie osservazioni fatte
        for i,oss in enumerate(self.listaOss):
            varianzeStazioniX=[]
            varianzeStazioniN=[]
            varianzeStazioniW=[]
            # Ciclo su tutte le stazioni
            for j in range(4):
                sommatoriaX=float(0)
                sommatoriaN=float(0)
                sommatoriaW=float(0)
                for prova in oss.indiciProve:
                    sommatoriaX+=pow((prova.indiciStazioni[j]["X"]-oss.medieIndici[j]["MediaX"]),2)
                    sommatoriaN+=pow((prova.indiciStazioni[j]["N"]-oss.medieIndici[j]["MediaN"]),2)
                    sommatoriaW+=pow((prova.indiciStazioni[j]["W"]-oss.medieIndici[j]["MediaW"]),2)
                varianzeStazioniX.append(sommatoriaX/(self.numProve-1))
                varianzeStazioniN.append(sommatoriaN/(self.numProve-1))
                varianzeStazioniW.append(sommatoriaW/(self.numProve-1))
            self.varianzeX.append(varianzeStazioniX)
            self.varianzeN.append(varianzeStazioniN)
            self.varianzeW.append(varianzeStazioniW)

    def stampaRisultati(self):
        """
        Stampa gli scarti delle medie delle varie osservazioni con relativa varianza
        :return:
        """
        print "\n\n*******STAMPA RISULTATI"
        for i,oss in enumerate(self.varianzeX):
            print "\nOSSERVAZIONE:",i
            for j,varStaz in enumerate(oss):
                print "----Per la stazione",j,"abbiamo:"
                print "VarianzaX:",varStaz
                print "VarianzaN:",self.varianzeN[i][j]
                print "VarianzaW:",self.varianzeW[i][j]



