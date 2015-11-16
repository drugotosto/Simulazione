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
        # Memorizzo la somma complessiva dei vari indici, di ogni stazione, per le varie osservazioni
        for oss in self.listaOss:
            for prova in oss.indiciProve:
                for i in range(len(prova.indiciStazioni)):
                    for j,indStaz in enumerate(prova.indiciStazioni):
                        if j==i:
                            oss.sommeIndici[i]["SommaX"]+=indStaz["X"]
                            oss.sommeIndici[i]["SommaN"]+=indStaz["N"]

        """
        DEVO CALCOLARMI LE MEDIE E VARIANZE DELLE VARIE OSSERVAZIONI
        """
        for i,oss in enumerate(self.listaOss):
            for somma in oss.sommeIndici:
                oss.medieIndici[i]["MediaX"]=somma["SommaX"]/self.numProve
                oss.medieIndici[i]["MediaN"]=somma["SommaN"]/self.numProve


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



