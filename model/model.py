import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap={}
        self._bestSet = None
        self._bestScore = 0
    def getSetAlbum(self, a1, dTOT):
        self._bestSet = None
        self._bestScore = 0
        connessa = nx.node_connected_component(self._grafo, a1)
        parziale=set([a1])
        connessa.remove(a1)
        self._ricorsione(parziale, connessa, dTOT)
        return self._bestSet, self.durataTot(self._bestSet)
    def _ricorsione(self, parziale, connessa, dTOT):
        # verificare se parziale è una sol ammissibile
        if self.durataTot(parziale)>dTOT:
            return
        # verificare se parziale è migliore del best

        if len(parziale)>self._bestScore:
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)
        # ciclo su nodi aggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                #rimanenti = copy.deepcopy(connessa)
                #rimanenti.remove(c)
                self._ricorsione(parziale, connessa, dTOT)
                parziale.remove(c)
    def durataTot(self, listOfNodes):
        dtot=0
        for n in listOfNodes:
            dtot+=n.durataA
        return toMinutes(dtot)
    def buildGraph(self, d):
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getAlbums(toMillisec(d)))
        self._idMap={a.AlbumId: a for a in list(self._grafo.nodes)}
        edges = DAO.getEdges(self._idMap)
        self._grafo.add_edges_from(edges)
    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._grafo, v0)
        durataTot = 0
        for album in conn:
            durataTot+=toMinutes(album.durataA)
        return len(conn), durataTot
    def graphDeatails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
    def getNodes(self):
        return list(self._grafo.nodes)
    def getGraphSize(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

def toMillisec(d):
    return d*60*1000
def toMinutes(d):
    return d/1000/60