from model.model import Model
model = Model()


model.build_graph(1980,'sphere')

for nodo in model.G.nodes():
    print(f"{nodo}")

for edge in model.G.edges(data=True):
    print(f"{edge}")
