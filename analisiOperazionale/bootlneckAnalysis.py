__author__ = 'maury'

import numpy as np

def calcoloVisite(md,ind):

    """ Visit vector is computed using
               V = VQ

         The Scipy library can solve only linear system
         in the form  A X = b

         So we transform the system in:
           VQ = V => VQ -V = 0
               => V (Q -I) = 0 => V Q' = 0

         then we have:
               V Q' = 0
         if we transpose the VQ' product, since Q is square, we have:
           (VQ').T = 0 <=> Q'.T V.T = 0

         The resulting system is not yet determined so we substitute
         an equation (let's say the first) with V_0 = 1"""

    # transition matrix
    q = np.array(md.q)
    # identity matrix
    i = np.identity(len(q))
    # transform into an homegeneus system
    q = q - i
    # create the ordinate vector
    b = np.zeros(len(q))
    # normalizing term (derived from the equation V_0 = 1)
    b[ind] = 1
    # convert the system to the form AX = 0
    qt = q.transpose()
    # substitutes the first equation with V_0
    qt[ind] = b
    # solve the system in the form AX = 0
    v = np.linalg.solve(qt, b)

    # Aggiorno il valore delle visite alle varie stazioni nel modello
    md.aggiornaVisite(v)
    return v

def calcoloDomande(md):
    visite=[]
    servizi=[]

    # Recupero delle visite di ogni stazione sotto forma di Array di numpy dal modello
    for staz in md.stazioni:
        visite.append(staz.visite)
    v=np.array(visite)

    # Recupero dei tempi di servizio delle varie stazioni sotto forma Array di numpy dal modello
    for staz in md.stazioni:
        servizi.append(staz.s)
    s=np.array(servizi)

    # Calcolo relative domande per le varie stazioni
    d=np.zeros(4)
    d=v*s

    # Aggiorna le varie domande per le varie stazioni nel modello
    md.aggiornaDomande(d)
    return d


def controlloStazione(md):
    x=[]
    for staz in md.stazioni:
        if  staz.tipo!="infinite":
            x.append(staz.domande)
        else:
            x.append(0)
    # Ritorna una nuova lista in cui le domande delle stazioni infinite server sono messe a 0
    return x


def calcoloU(dMax,md,indice_rif):
    return (1/dMax*md.stazioni[indice_rif].s)*100