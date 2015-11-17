__author__ = 'maury'

# Numero di eventi da settare inizialmente in coda
nj=4

# Indice della stazione in cui andare ad inserire gli eventi in fase di inizializzazione
indStaz=0

# Tempo di schedulazione fine simulazione
tFine=65000

# Tempo estremo termine simulazione per evitare LOOP
tMax=67000

# File da cui andare a recuperare i dati
pathDati="exponential.json"

# Seme da utilizzare per l'inizializzazione del generatore di numeri casuali
debug=False

# Massimo indice da utilizzare come indice per pescare un numero casuale primo da utilizzare come seme
maxRange=100000

# Numero di Run di simulazione da eseguire
numRun=100

# Intervallo di osservazioni per calcolo del fine Transitorio
TempOss=20000
