__author__ = 'maury'

import numpy as np

class Osservazione():
    def __init__(self,sim):
        self.indiciProve=[]
        self.sommeIndici=[]
        for i in range(len(sim.md.stazioni)):
            self.sommeIndici.append({"SommaX":np.float(0),"SommaN":np.float(0)})
        self.medieIndici=[]
        for i in range(len(sim.md.stazioni)):
            self.medieIndici.append({"MediaX":np.float(0),"MediaN":np.float(0)})

class Prova():
    def __init__(self):
        self.indiciStazioni=[]