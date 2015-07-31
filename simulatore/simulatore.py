__author__ = 'maury'

from simulatore.struttureDati.evento import *

class Simulatore():
    def __init__(self,md):
        self.eventList=[]
        self.freeList=[]
        self.time=0.0
        self.md=md

    def inizialization(self):
        pass

    def engine(self):
        pass

    def report(self):
        pass