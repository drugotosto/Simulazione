__author__ = 'maury'

# Numero di eventi da settare inizialmente in coda
nj=4

# Indice della stazione in cui andare ad inserire gli eventi in fase di inizializzazione
indStaz=3

# Tempo di schedulazione fine simulazione
tFine=40000

# Tempo estremo termine simulazione per evitare LOOP
tMax=55000

# File da cui andare a recuperare i dati
pathDati="exponential.json"

# Seme da utilizzare per l'inizializzazione del generatore di numeri casuali
debug=False

# Massimo indice da utilizzare come indice per pescare un numero casuale primo da utilizzare come seme
maxRange=100000

# Setto il numero iniziale di prove di simulazioni differenti da utilizzare (n0)
proveN0=5

# Tempo di fine transizione
fineTrans=0
