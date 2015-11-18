__author__ = 'maury'

# Numero di eventi da settare inizialmente in coda
nj=2

# Indice della stazione in cui andare ad inserire gli eventi in fase di inizializzazione
indStaz=0

# Tempo di schedulazione fine simulazione
tFine=20000

# Tempo estremo termine simulazione per evitare LOOP
tMax=25000

# File da cui andare a recuperar
# e i dati
pathDati="exponential.json"

# Seme da utilizzare per l'inizializzazione del generatore di numeri casuali
debug=False

# Massimo indice da utilizzare come indice per pescare un numero casuale primo da utilizzare come seme
maxRange=100000

# Setto il numero iniziale di prove di simulazioni differenti da utilizzare (n0)
proveN0=2

# Tempo di fine transizione
fineTrans=0.0
