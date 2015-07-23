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

        print "La lista di stazioni con corrispondente valore da inserire nella matrice Q in output per lo stato", stato.stato,"di indice",i,"e:", statiOut

        # Costruzione di una riga alla volta per la matrice Q
        costruzioneRigaQ(i,statiOut,q)
    return q


# Per ogni stato di partenza in base alla matrice di transizione ritorna i corrispondenti stati in output
def ricercaStatiUscita(stato, md):
    print "\n\nConsidero lo stato: ",stato.stato,"di tipo",stato.tipo
    listaStat = []
    # Lo stato preso in considerazione risulta essere "normale"
    if stato.tipo=="normale":
        for j,n in enumerate(stato.stato):
            print "---Per la stazione: ", j
            mapStatoVal=[]
            col = []
            if n != 0:
                # Recupero tutti gli indici delle colonne per cui la matrice di P ha un valore !=0 (senza tener conto del ciclo 1->1)
                col = [i for i, val in enumerate(md.q[j]) if val != 0.0 and i != j]
                print "Da stazione :", j, " a stazione", col

                # Costruisco i relativi stati in output per ogni possibile partenza dalle varie stazioni
                valQ=0.0
                for i,val in enumerate(col):
                    stazOut=list(stato.stato)
                    stazOut[j]=stazOut[j]-1
                    stazOut[val]=stazOut[val]+1

                    #Calcolo del corrispondente valore da inserire successivamente nella matrice Q
                    # j: indice stazione di partenza
                    # val: indice stazione arrivo
                    if  md.stazioni[j].tipo=="server":
                        valQ=(1.0/md.stazioni[j].s)*md.q[j][val]

                    elif md.stazioni[j].tipo=="infinite":
                        valQ=(1.0/(md.stazioni[j].s/float(stato.stato[j])))*md.q[j][val]

                    # CASO IN CUI SI FINISCE IN UNA STAZIONE SERVER/INFINITE NORMALE
                    if md.stazioni[val].tipo!="erlang":
                        print "Si finisce in una stazione Server/Infinite"
                        """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                        mapStatoVal=[ricercaOggettoStato(md,tuple(stazOut),"normale"),valQ]
                        print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato

                    # CASO IN CUI SI FINISCE IN UNA STAZIONE ERLANG
                    else:
                        print "Si finisce in una stazione Erlang"
                        """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                        mapStatoVal=[ricercaOggettoStato(md,tuple(stazOut),"erlang",3),valQ]
                        print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato,",listStazErl:",md.spazioStati[mapStatoVal[0]].listStazErl

                    listaStat.append(mapStatoVal)
                    # Rimozione celle vuote
                    mapStatoVal=[x for x in listaStat if x != []]
                    listaStat=[x for x in listaStat if x != []]

    # Lo stato preso in considerazione risulta essere "Erlang"
    else:
        for j,n in enumerate(stato.stato):
            print "---Per la stazione: ", j
            mapStatoVal=[]
            col = []
            if n!=0:
                # PARTENZA da una stazione erlang con S>1 e quindi tocca scalare..
                if (md.stazioni[j].tipo=="erlang")and(stato.listStazErl[0]['stadK']>1):
                    print "Sono nello stato:",stato.listStazErl,"basta scalare"
                    valQ=(1.0/(md.stazioni[j].s/md.stazioni[stato.listStazErl[0]['indStaz']].k))

                    mapStatoVal=[ricercaOggettoStato(md,tuple(stato.stato),"erlang",stato.listStazErl[0]['stadK']-1),valQ]
                    print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato,",listStazErl:",md.spazioStati[mapStatoVal[0]].listStazErl

                    listaStat.append(mapStatoVal)
                    # Rimozione celle vuote
                    mapStatoVal=[x for x in listaStat if x != []]
                    listaStat=[x for x in listaStat if x != []]

                # PARTENZA da una stazione erlang con S==1 e quindi tocca cercare nuovi stati
                elif (md.stazioni[j].tipo=="erlang")and(stato.listStazErl[0]['stadK']==1):
                    print "Sono nello stato:",stato.listStazErl,"devo andare a scoprire in quale nuovo stato finiro!"

                    # Recupero tutti gli indici delle colonne per cui la matrice di P ha un valore !=0 (senza tener conto del ciclo 1->1)
                    col = [i for i, val in enumerate(md.q[j]) if val != 0.0 and i != j]
                    print "Da stazione :", j, " a stazione", col

                    # Costruisco i relativi stati in output per ogni possibile partenza dalle varie stazioni
                    valQ=0.0
                    for i,val in enumerate(col):
                        stazOut=list(stato.stato)
                        stazOut[j]=stazOut[j]-1
                        stazOut[val]=stazOut[val]+1

                        # Calcolo valore di uscita dallo stato preso in considerazione da inserire in Q
                        valQ=(1.0/(md.stazioni[j].s/md.stazioni[stato.listStazErl[0]['indStaz']].k))*md.q[j][val]

                        # CASO IN CUI SI N==1 (era l'ultima persona presente nella stazione Erlang)
                        if stato.stato[j]==1:
                            print "Era l'ultima persona presente nella stazione Erlang!"
                            """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                            mapStatoVal=[ricercaOggettoStato(md,tuple(stazOut),"normale"),valQ]
                            print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato
                        # CASO IN CUI SI N>1 (non era l'ultima persona)
                        else:
                            print "Si diminusce di 1 il numero di persone nella stazione Erlang"
                            """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                            mapStatoVal=[ricercaOggettoStato(md,tuple(stazOut),"erlang",3),valQ]
                            print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato,",listStazErl:",md.spazioStati[mapStatoVal[0]].listStazErl

                        listaStat.append(mapStatoVal)
                        # Rimozione celle vuote
                        mapStatoVal=[x for x in listaStat if x != []]
                        listaStat=[x for x in listaStat if x != []]

                # PARTENZA da una stazione non Erlang
                elif md.stazioni[j].tipo!="erlang":
                    print "Sono nello stato:",stato.listStazErl,"partenza da una stazione non Erlang (caso normale)"

                    # Recupero tutti gli indici delle colonne per cui la matrice di P ha un valore !=0 (senza tener conto del ciclo 1->1)
                    col = [i for i, val in enumerate(md.q[j]) if val != 0.0 and i != j]
                    print "Da stazione :", j, " a stazione", col

                    for val in col:
                        # Costruisco i relativi stati in output per ogni possibile partenza dalle varie stazioni
                        valQ=0.0
                        for i,val in enumerate(col):
                            stazOut=list(stato.stato)
                            stazOut[j]=stazOut[j]-1
                            stazOut[val]=stazOut[val]+1

                            #Calcolo del corrispondente valore da inserire successivamente nella matrice Q
                            # j: indice stazione di partenza
                            # val: indice stazione arrivo
                            if  md.stazioni[j].tipo=="server":
                                valQ=(1.0/md.stazioni[j].s)*md.q[j][val]

                            elif md.stazioni[j].tipo=="infinite":
                                valQ=(1.0/(md.stazioni[j].s/float(stato.stato[j])))*md.q[j][val]

                            # UGUALE SE SI FINISCE IN UNA STAZIONE SERVER/INFINITE o ERLANG
                            print "Si finisce in una stazione Server/Infinite"
                            """Funzione per andare alla ricerca dell'oggetto Stato che contiene lo stato=stazOut"""
                            mapStatoVal=[ricercaOggettoStato(md,tuple(stazOut),"erlang",stato.listStazErl[0]['stadK']),valQ]
                            print "Lo stato out e:",md.spazioStati[mapStatoVal[0]].stato,",listStazErl:",md.spazioStati[mapStatoVal[0]].listStazErl

                            listaStat.append(mapStatoVal)
                            # Rimozione celle vuote
                            mapStatoVal=[x for x in listaStat if x != []]
                            listaStat=[x for x in listaStat if x != []]

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


"""
DA QUI IN POI UGUALE A MASTER
"""

# Costruzione di una riga alla volta della matrice Q
def costruzioneRigaQ(i,listStatVel,q):
    som=0.0
    for statVel in listStatVel:
        q[i][statVel[0]]=statVel[1]
        som+=statVel[1]
    # Sulla diagonale ci deve essere -SOMMA TUTTI ELEMENTI
    q[i][i]=-som

# Risoluzione sistema di eq. lineari per il calcolo della distribuzione di prob dei vari stati
def risoluzioneSistema(q):
    q = q.transpose()
    q[-1] = np.ones(len(q))
    b = np.zeros(len(q))
    b[-1] = 1
    return np.linalg.solve(q, b)

