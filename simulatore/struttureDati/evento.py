__author__ = 'maury'

from classTools import Display
from itertools import count


class Evento(Display,object):
    _ids=count(1)

    def __init__(self,genT,serT,occT,tipo,idJob,idStaz):
        """
        Settaggio dei parametri al nuovo evento appena creato
        :param genT: Tempo di generazione dell'evento
        :param serT: Tempo di servizio generato
        :param occT: Tempo in cui verra schedulato l'evento
        :param tipo: Tipologia dell'evento
        :param idJob: Id del job al quale l'evento si riferisce
        :param idStaz: Id della stazione al quale si riferisce l'evento
        """
        self.genT=genT
        self.serT=serT
        self.occT=occT
        self.tipo=tipo
        self.idJob=idJob
        self.idStaz=idStaz
        self.idEv=self._ids.next()

    def __cmp__(self, other):
        """
        Overload del confronto tra Eventi in base al tempo di schedulazione
        :param other: Altro oggetto Evento con cui si effettua il confronto
        :return: risultato del confronto
        """
        return cmp(self.occT,other.occT)

    def settaggioValori(self,genT,serT,occT,tipo,idJob,idStaz):
        """
        Risettaggio dei parametri dati all'evento appena prelevato dalla freeList del simulatore
        :param genT: Tempo di generazione dell'evento
        :param serT: Tempo di servizio generato
        :param occT: Tempo in cui verra schedulato l'evento
        :param tipo: Tipologia dell'evento
        :param idJob: Id del job al quale l'evento si riferisce
        :param idStaz: Id della stazione al quale si riferisce l'evento
        """
        self.genT=genT
        self.serT=serT
        self.occT=occT
        self.tipo=tipo
        self.idJob=idJob
        self.idStaz=idStaz
        self.idEv=self._ids.next()


if __name__ == '__main__':
    ev1=Evento(0.0,3.0,"null","coda",1,0)
    ev2=Evento(0.0,4.0,4.0,"partenza",2,0)
    ev3=Evento(1.0,2.0,"null","coda",3,0)

    if(ev1<ev2):
        print "L'evento 1 accade prima dell'evento 2"
    else:
        print "L'evento 2 accade prima l'evento 1"

    print "STAMPA Ev1:",ev1
    """
       Without arguments, return the list of names in the current local scope.
       With an argument, attempt to return a list of valid attributes for that object
       Non vengono stampati gli attributi ereditati dalle classi.
    """
    print "DIR:",dir(ev1)
    """
       Return the __dict__ attribute for a module, class, instance, or any other
       object with a __dict__ attribute (Caso particolare per classi Python 3.x).
       Non vengono stampati gli attributi ereditati dalle classi.
    """
    print "VARS:",vars(ev1)

    print "STAMPA Ev2:",ev2
    print "STAMPA Ev2:",ev3