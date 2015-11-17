__author__ = 'maury'

import numpy as np

class Transitorio():
    def __init__(self):
        self.numProve=0
        self.indOss=0
        self.listaOss=[]
        self.varianze=[]

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
        for i,oss in enumerate(self.listaOss):
            SommaMedieX=[]
            for j in range(len(self.listaOss[0].medieIndici)):
                SommaMedieX.append(np.float(0))
            SommaMedieN=[]
            for j in range(len(self.listaOss[0].medieIndici)):
                SommaMedieN.append(np.float(0))
            listaOss=[oss2 for j,oss2 in enumerate(self.listaOss) if j<=i]
            listaMedie=[oss2.medieIndici for oss2 in listaOss]

            listaOssMedieGen=[]
            # Sommo le medie delle prime i+1 osservazioni
            for k,medie in enumerate(listaMedie):
                for j,medieStaz in enumerate(medie):
                    SommaMedieX[j]+=medieStaz["MediaX"]
                    SommaMedieN[j]+=medieStaz["MediaN"]
                if(i==len(self.listaOss)-1):
                    # print "\nSommaMedieX:",SommaMedieX
                    listaMedieGen=[mediaStaz/(k+1) for mediaStaz in SommaMedieX]
                    listaOssMedieGen.append(listaMedieGen)

            if(i==len(self.listaOss)-1):
                """print "\nPrime",i+1,"osservazioni:"
                for i,medie in enumerate(listaMedie):
                    print "\nMedie Osservazione",i,":",medie
                print "\n"
                for i,listaMedieGen in enumerate(listaOssMedieGen):
                    print "\nMedie generali Osservazione",i,":",listaMedieGen"""

                for j in range(len(self.listaOss[0].medieIndici)):
                    sommatoria=np.float(0)
                    for i,medie in enumerate(listaMedie):
                        sommatoria+=pow(medie[j]["MediaX"]-listaOssMedieGen[-1][j],2)
                    self.varianze.append(sommatoria/len(self.listaOss))

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
        print "\nLista Varianze sulla X rilevate all'ultimo passo per le varie stazioni:",self.varianze



