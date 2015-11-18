__author__ = 'maury'

class Prova():
    def __init__(self):
        """
        Costruttore di una singola prova eseguita
        :return:
        """
        self.partenzeStazioni=[]
        self.areaStazioni=[]

    def registraDatiProva(self,sim):
        """
        Vado a registrare per tutte le stazioni i valori di Partenze e Area
        :return:
        """
        self.partenzeStazioni=[staz.partenze for staz in sim.md.stazioni]
        self.areaStazioni=[staz.area for staz in sim.md.stazioni]
