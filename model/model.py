from database.dao import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.G=nx.Graph()

        self._lista_stati=[]
        self.id_map={}

        self._lista_stati_vicini=[]
        self.id_map_vicini={}
        self.peso_map={}

    @staticmethod
    def load_years():
        return DAO.get_years()

    @staticmethod
    def load_shapes(year):
        return DAO.get_shapes(year)

    def build_graph(self,year,shape):
        self.G.clear()

        self._lista_stati=DAO.get_all_states()
        self.id_map={}
        for state in self._lista_stati:
            self.id_map[state.id.upper()]=state

        self.G.add_nodes_from(self._lista_stati) # i nodi sono gli oggetti stato

        self.peso_map=DAO.get_edges_weight(year,shape)

        self._lista_stati_vicini=DAO.get_stati_vicini()
        self.id_map_vicini={}
        for s in self._lista_stati_vicini:
            self.id_map_vicini[s[0]]=s
            self.id_map_vicini[s[1]]=s

        for s in self._lista_stati_vicini:
            if s[0] in self.id_map and s[1] in self.id_map:
                stato1=self.id_map[s[0]]
                stato2=self.id_map[s[1]]
                # if self.G.has_node(stato1) and self.G.has_node(stato2):
                peso=self.peso_map.get(s[0], 0) + self.peso_map.get(s[1], 0)
                self.G.add_edge(stato1, stato2,weight=peso)
                    # self.G[stato1][stato2]['weight']=peso

    def get_num_nodes(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.number_of_edges()

    def weight_archi_adiacenti(self):
        result=[]
        for s in self._lista_stati: # per ogni stato nei nodi
            somma=0
            adiacenti=list(self.G.neighbors(s))
            for a in adiacenti:
                peso=self.G[s][a]['weight']
                somma+=peso
            result.append((s,somma))
            result.sort(key=lambda x: x[0].id)
        return result