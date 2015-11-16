__author__ = 'maury'

import numpy as np

class Transitorio():
    def __init__(self):
        self.numProve=0
        self.indOss=0
        self.listaOss=[]

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

        # Memorizzo la somma complessiva dei vari indici, di ogni stazione, per le varie osservazioni
        for oss in self.listaOss:
            for prova in oss.indiciProve:
                for j,indStaz in enumerate(prova.indiciStazioni):
                        oss.sommeIndici[j]["SommaX"]+=indStaz["X"]
                        oss.sommeIndici[j]["SommaN"]+=indStaz["N"]

        # Calcolo delle medie degli indici di ogni stazione rispetto alle varie osservazioni fatte
        for oss in self.listaOss:
            for j,somma in enumerate(oss.sommeIndici):
                oss.medieIndici[j]["MediaX"]=somma["SommaX"]/self.numProve
                oss.medieIndici[j]["MediaN"]=somma["SommaN"]/self.numProve

        # Calcolo della Varianza di ogni indice per ogni stazione rispetto alle osservazioni fatte
        for oss in self.listaOss:
            for j,media in enumerate(oss.medieIndici):
                oss.varianzeIndici[j]["MediaX"]=media["MediaX"]
                oss.medieIndici[j]["MediaN"]=somma["SommaN"]/self.numProve


    def stampaRisultati(self):
        """
        Stampa gli scarti delle medie delle varie osservazioni con relativa varianza
        :return:
        """
        print "\n\n*******STAMPA RISULTATI"
        for i,oss in enumerate(self.listaOss):
            print "\nOSSERVAZIONE:",i
            for j,medie in enumerate(oss.medieIndici):
                print "----Per la stazione",j,"abbiamo:"
                print "MEDIAX:",medie["MediaX"]
                print "MEDIAN:",medie["MediaN"]



