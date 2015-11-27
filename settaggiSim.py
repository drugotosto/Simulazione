__author__ = 'maury'

# Numero di eventi da settare inizialmente in coda
nj=2

# Indice della stazione in cui andare ad inserire gli eventi in fase di inizializzazione
indStaz=3

# Tempo di schedulazione fine simulazione
tFine=161000

# Tempo estremo termine simulazione per evitare LOOP
tMax=165000

# File da cui andare a recuperare i dati
pathDati="tracce/exponential.json"

# Seme da utilizzare per l'inizializzazione del generatore di numeri casuali
debug=False

# Massimo indice da utilizzare come indice per pescare un numero casuale primo da utilizzare come seme
maxRange=100000

# Numero di Run di simulazione da eseguire
numRun=1000

# Intervallo di osservazioni per calcolo del fine Transitorio
TempOss=20000
