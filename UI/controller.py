import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # VEDERE SOTTO
        # TODO

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        year=self._view.dd_year.value
        shape=self._view.dd_shape.value

        if year is None:
            self._view.show_alert('Inserire un anno!')
            return
        if shape is None:
            self._view.show_alert('Inserire una forma!')
            return

        self._model.build_graph(int(year), shape)

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f'Numero di vertici: {self._model.get_num_nodes()} Numero di archi: {self._model.get_num_edges()}')
        )
        self.show_weights()
        self._view.update()
        # TODO

    def show_weights(self):
        result = self._model.weight_archi_adiacenti()
        for r in result:
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f'Nodo {r[0].id} somma pesi su archi= {r[1]}')
            )

        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

    def fill_years(self):
        """ Popola il dropdown con gli anni """
        self._view.dd_year.options.clear()
        self._view.dd_year.value = None

        all_years = self._model.load_years()

        self._view.dd_year.options = [ft.dropdown.Option(key=y, text=y) for y in all_years]

        self._view.dd_year.update()

    def get_selected_year(self,e):
        """Handler per gestire la selezione di un anno"""
        selected_year=self._view.dd_year.value
        if selected_year is None:
            self._view.show_alert('Selezionare un anno!')
            return

        self.fill_shapes(int(selected_year))

        self._view.update()

    def fill_shapes(self,selected_year):
        self._view.dd_shape.options.clear()
        self._view.dd_shape.value = None

        all_shapes=self._model.load_shapes(int(self._view.dd_year.value))

        self._view.dd_shape.options=[ft.dropdown.Option(key=s,text=s) for s in all_shapes]

        self._view.dd_shape.update()

    def get_selected_shape(self,e):
        selected_shape=self._view.dd_shape.value
        if selected_shape is None:
            self._view.show_alert('Selezionare una forma!')
            return
        self._view.update()

