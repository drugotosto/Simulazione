__author__ = 'maury'
import itertools
import numpy as np
from settaggi import m


# Generazione dello spazio degli stati valido anche in presenza di stazioni con distribuzione di Erlang
def generaSpazioStati(md,n):
    # Prodotto Cartesiano di tutti i possibili elementi dati dall'array (0,1,2,3,...15)
    comb = list(itertools.product(range(0, n + 1), repeat=m))
    # Si sottraggono poi tutti questi elementi la cui somma non arriva ad un totale di n
    comb = [val for val in comb if sum(val) == n]
    print "Spazio Originale:",comb,"\nlung:",len(comb)
    # Recupero lista degli indici stazioni che sono di tipo erlang_k
    ind_staz=[i for i,staz in enumerate(md.stazioni) if staz.tipo=="erlang"]
    z=0
    # Ciclo sulla lista degli spazi "originali" per sostituire quelli in cui la stazione con distribuzione ERLANG ha n>0
    for i,stat in enumerate(comb):
        for j in range(len(md.stazioni)):
            # Controllo se lo stato nella posizione corrispondente "j" sia quella della stazione con distr. Erlang e se ha numero elementi >0
            if (j in ind_staz)and(stat[j]>0):
                if(i>=z):
                    comb[i:i+1]=[]
                    # Vado a sostituire lo stato (x,x,x,x) con la serie [(x,x,x,x),ind],[(x,x,x,x),ind] data dalla funzione
                    z=generaStatiErlang(md,comb,i,stat,j)
    return comb

# Sostituizione stato "originale" con stati erlanghiani...
def generaStatiErlang(md,comb,i,stat,j):
    statiIns=[(stat,z) for z in range(1,md.stazioni[j].k+1)]
    for stato in statiIns:
        comb.insert(i,stato)
        i+=1
    return i

# Metodo per la creazione della matrice Q
def creazioneMatriceQ(md):
    q = np.zeros((len(md.spazioStati), len(md.spazioStati)))

    # Ciclo sullo spazio degli stati e per ogni stato:
    #     - Considero i valori per ogni posizione !=0 vado a vedere sulla matrice P tutti le colonne della
    #       corrispondente riga che hanno valore !=0 capendo cosi su quale stato ci si riesce a spostare...
    #     - Effettuo la conversione dei vari stati trovati al passo precedente recuperando l'indice della
    #       colonna della Q su cui andare ad inserire il corrispondente valore calcolato a parte.

    # - Eseguo la trasposta della matrice Q per passare da piGreco*Q=0 -> Q*piGreco=0 e setto la
    # condizione iniziale

    # print "P:", md.q

    # Ciclo su tutto lo spazio degli stati
    for i, stato in md.spazioStati.items():
        # Per ogni stato ritorna i corrispondenti la lista degli stati in output
        statiOut=ricercaStatiUscita(stato, md)

        print "La lista di stazioni con corrispondente valore da inserire nella matrice Q in output per lo stato", stato[0], "e:", statiOut

        #metodo che ritorna una lista di stati destinatari associati allo stato di partenza con relative velocita
        listStatVel=mappStatiVel(md,stato[0],statiOut)

        print "Lo stato ha indice:",i ,"e la lista statVel:",listStatVel

        # Costruzione di una riga alla volta per la matrice Q
        costruzioneRigaQ(i,listStatVel,q)
    return q


# Per ogni stato di partenza in base alla matrice di transizione ritorna i corrispondenti stati in output
def ricercaStatiUscita(stato, md):
    print "\n\nPer lo stato: ", stato[0]
    # Controllo il numero di persone presenti ad ogni stazione
    listaStat = []
    for j, n in enumerate(stato[0]):
        print "---Per la stazione: ", j
        col = []
        if n != 0:
            # Recupero tutti gli indici delle colonne per cui la matrice di P ha un valore !=0 (senza tener conto del ciclo 1->1)
            col = [i for i, val in enumerate(md.q[j]) if val != 0.0 and i != j]
            print "Da stato :", j, " a stato", col

        # Costruisco i relativi stati in output per ogni possibile partenza dalle varie stazioni
        listaStazOut = [[]]
        valQ=0.0
        for i, val in enumerate(col):
            stazOut = list(stato[0])
            stazOut[j] = stazOut[j] - 1
            stazOut[val] = stazOut[val] + 1

            #Calcolo del corrispondente valore da inserire successivamente nella matrice Q
            # j: indice stazione di partenza
            # val: indice stazione arrivo
            if  md.stazioni[j].tipo=="server":
                valQ=(1.0/md.stazioni[j].s)*md.q[j][val]

            elif md.stazioni[j].tipo=="infinite":
                valQ=(1.0/(md.stazioni[j].s/float(stato[0][j])))*md.q[j][val]

            mapStatoVal=(stazOut,valQ)
            listaStazOut.append(mapStatoVal)

        listaStat.extend((listaStazOut))
        # Rimozione celle vuote
        listaStat=[x for x in listaStat if x != []]
    return listaStat


def mappStatiVel(md,stato,statiOut):
    # Ricerco riga della matrice Q su cui andare a settare i valori
    riga = [key for key, value in md.spazioStati.items() if value[0] == stato]
    print "la riga per lo stato", stato, "e:", riga[0]

    listStatVel=[[]]
    # Ricerco le diverse colonne della matrice Q e setto con il corrispondente valore
    for statOut in statiOut:
        # Metodo per riuscire a trovare l'indice relativo alla colonna della matrice Q su cui poi andare a settare il giusto valore
        colonna = [key for key, value in md.spazioStati.items() if value[0] == tuple(statOut[0])]
        print "La colonna per lo stato ", statOut, "e:", colonna[0]

        listStatVel.append([colonna[0],statOut[1]])
         # Rimozione celle vuote
        listStatVel=[x for x in listStatVel if x != []]

    # print "Lista stati velocita: ",listStatVel
    return listStatVel

# Costruzione di una riga alla volta della matrice Q
def costruzioneRigaQ(i,listStatVel,q):
    som=0.0
    for statVel in listStatVel:
        q[i][statVel[0]]=statVel[1]
        som+=statVel[1]
    q[i][i]-=som

# Risoluzione sistema di eq. lineari per il calcolo della distribuzione di prob dei vari stati
def risoluzioneSistema(q):
    q = q.transpose()
    q[-1] = np.ones(len(q))
    b = np.zeros(len(q))
    b[-1] = 1
    return np.linalg.solve(q, b)
