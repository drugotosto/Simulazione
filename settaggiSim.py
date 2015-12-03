__author__ = 'maury'

# Numero di eventi da settare inizialmente in coda
nj=44

# Indice della stazione in cui andare ad inserire gli eventi in fase di inizializzazione
indStaz=0

# Tempo di schedulazione fine simulazione
tFine=160000

# Tempo estremo termine simulazione per evitare LOOP
tMax=160001

# File da cui andare a recuperare i dati
pathDati="tracce/misto.json"

# Seme da utilizzare per l'inizializzazione del generatore di numeri casuali
debug=False

# Massimo indice da utilizzare come indice per pescare un numero casuale primo da utilizzare come seme
maxRange=100000

# Tempo di fine transizione
fineTrans=100000

# Setto il numero iniziale di prove di simulazioni differenti da utilizzare (n0)
proveN0=15

# Setto il livello di precisione e livello di confidenza (alfa) desiderati
precisione,alfa=0.1,0.05

# Numero di simulazioni totali da effettuare
simNumber=1

# Numero di Simulazioni in cui valore teorico risulta contenuto all'interno dell'intervallo trovato
numSimDentro=0