__author__ = 'maury'

class Evento():
    numEv=1
    def __init__(self,genT,serT,occT,tipo,idJob,idStaz):
        self.genT=genT
        self.serT=serT
        self.occT=occT
        self.tipo=tipo
        self.idJob=idJob
        self.idStaz=idStaz
        self.idEv=Evento.numEv
        Evento.numEv+=1

    def __cmp__(self, other):
        return cmp(self.occ,other.occ)

    # Forma di stampa personalizzata che recupera anche gli attributi delle classi(con annessa ereditarieta)
    def __repr__(self):
        chiavi=[nome for nome in dir(self) if not nome.startswith('__')]
        valori=[]
        for ch in chiavi:
            valori.append(getattr(self,ch))
        return str(dict(zip(chiavi,valori)))



if __name__ == '__main__':
    ev1=Evento(1,0,'transizione',3.56)
    ev2=Evento(1,3,'transizione',2.70)

    if(ev1>ev2):
        print "L'evento 1 accade dopo l'evento 2"
    else:
        print "L'evento 2 accade dopo l'evento 1"

    print "STAMPA:",ev1
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