__author__ = 'maury'

import numpy as np

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
        # Per ogni stato ritorna la lista degli stati in output associata al corrispondete tasso d'uscita
        statiOut=ricercaStatiUscita(stato,md)

        print "La lista di stazioni con corrispondente valore da inserire nella matrice Q in output per lo stato", stato.stato, "e:", statiOut

        #metodo che ritorna una lista di stati destinatari associati allo stato di partenza con relative velocita
        # listStatVel=mappStatiVel(md,stato[0],statiOut)

        # print "Lo stato ha indice:",i ,"e la lista statVel:",listStatVel

        # Costruzione di una riga alla volta per la matrice Q
        # costruzioneRigaQ(i,listStatVel,q)
    return q


# Per ogni stato di partenza in base alla matrice di transizione ritorna i corrispondenti stati in output
def ricercaStatiUscita(stato, md):
    print "\n\nConsidero lo stato: ",stato.stato,"di tipo",stato.tipo
    listaStat = []
    # Lo stato preso in considerazione risulta essere "normale"
    if stato.tipo=="normale":
        for j, n in enumerate(stato.stato):
            print "---Per la stazione: ", j
            col = []
            if n != 0:
                # Recupero tutti gli indici delle colonne per cui la matrice di P ha un valore !=0 (senza tener conto del ciclo 1->1)
                col = [i for i, val in enumerate(md.q[j]) if val != 0.0 and i != j]
                print "Da stato :", j, " a stato", col

                for val in col:
                    # Costruisco i relativi stati in output per ogni possibile partenza dalle varie stazioni
                    valQ=0.0
                    for i, val in enumerate(col):
                        stazOut = list(stato.stato)
                        stazOut[j] = stazOut[j] - 1
                        stazOut[val] = stazOut[val] + 1

                        #Calcolo del corrispondente valore da inserire successivamente nella matrice Q
                        # j: indice stazione di partenza
                        # val: indice stazione arrivo
                        if  md.stazioni[j].tipo=="server":
                            valQ=(1.0/md.stazioni[j].s)*md.q[j][val]

                        elif md.stazioni[j].tipo=="infinite":
                            valQ=(1.0/(md.stazioni[j].s/float(stato.stato[j])))*md.q[j][val]

                        # CASO IN CUI SI FINISCE IN UNO STATO NORMALE
                        if md.stazioni[val].tipo!="erlang":
                            print "Si finisce in uno stato normale"
                            """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                            mapStatoVal=(ricercaOggettoStato(md,tuple(stazOut),"normale"),valQ)
                            print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato

                        # CASO IN CUI SI FINISCE IN UNO STATO ERLANG
                        else:
                            print "Si finisce in uno stato Erlang"
                            """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                            mapStatoVal=(ricercaOggettoStato(md,tuple(stazOut),"erlang",3),valQ)
                            print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato,",listStazErl:",md.spazioStati[mapStatoVal[0]].listStazErl

                        listaStat.append(mapStatoVal)
                        # Rimozione celle vuote
                        listaStat=[x for x in listaStat if x != []]

    # Lo stato preso in considerazione risulta essere "Erlang"
    else:
        print "Lo stato preso in considerazione e di Erlang"


    return listaStat

# Ricerca dell'oggetto Stato corrispondente a quello cercato e del tipo specifico
def ricercaOggettoStato(md,stazOut,tipo,k=0):
    for i,stato in md.spazioStati.items():
        # La chiamata e stata fatta per la ricerca di uno stato Erlang
        if (k!=0)and(stato.tipo=="erlang"):
            if (stato.stato==stazOut)and(stato.tipo==tipo)and(stato.listStazErl[0]['stadK']==k):
                return i
        # Chiamata fatta per uno stato "normale"
        else:
            if (stato.stato==stazOut)and(stato.tipo==tipo):
                return i

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

