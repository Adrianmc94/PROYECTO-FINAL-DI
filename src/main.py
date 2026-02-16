import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import conexionBD as db
# Importamos as dúas clases de fiestras desde formularios
from formularios import VentanaEvento, VentanaResumo


class AppPrincipal(Gtk.Window):
    """
    Clase principal da aplicación (Fiestra 1).
    Xestiona o TreeView e as operacións CRUD principais.
    """

    def __init__(self):
        super().__init__(title="Xestor de Eventos DAM - Edición 2026")
        self.set_default_size(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Contedor principal con marxes
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=15)
        self.add(vbox)

        # --- SECCIÓN SUPERIOR: TÁBOA ---
        # Frame para agrupar visualmente a táboa (Requisito de Deseño)
        frame_taboa = Gtk.Frame(label=" Listado de Eventos ")
        vbox.pack_start(frame_taboa, True, True, 0)

        # ListStore: ID(int), Nome(str), Tipo(str), Cat(int), Prio(str), Notas(str)
        self.store = Gtk.ListStore(int, str, str, int, str, str)
        self.tree = Gtk.TreeView(model=self.store)

        columnas = ["ID", "Nome", "Tipo", "Catering", "Prioridade", "Notas"]
        for i, tit in enumerate(columnas):
            render = Gtk.CellRendererText()
            # Permitir edición directa no nome para punto extra
            if i == 1:
                render.set_property("editable", True)
                render.connect("edited", self.on_edicion_directa)

            col = Gtk.TreeViewColumn(tit, render, text=i)
            col.set_resizable(True)
            col.set_sort_column_id(i)  # Permite ordenar ao facer clic na cabeceira
            self.tree.append_column(col)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.tree)
        frame_taboa.add(scroll)

        # --- SECCIÓN INFERIOR: CONTROL ---
        # Separador visual
        vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)

        hbox = Gtk.Box(spacing=10)
        vbox.pack_end(hbox, False, False, 0)

        self.btn_add = Gtk.Button(label="Engadir Evento")
        self.btn_add.connect("clicked", self.on_add)
        hbox.pack_start(self.btn_add, True, True, 0)

        self.btn_resumo = Gtk.Button(label="Ver Estatísticas")
        self.btn_resumo.connect("clicked", self.on_ver_resumo)
        hbox.pack_start(self.btn_resumo, True, True, 0)

        self.btn_del = Gtk.Button(label="Eliminar Seleccionado")
        self.btn_del.connect("clicked", self.on_del)
        hbox.pack_start(self.btn_del, True, True, 0)

        # Inicialización
        db.inicializar_bd()
        self.refrescar()
        self.show_all()

    def refrescar(self):
        """Actualiza os datos da táboa dende a BD."""
        self.store.clear()
        for r in db.CRUD("R"):
            self.store.append(list(r))

    def on_add(self, _):
        """Abre a Fiestra 2 (Formulario de entrada)."""
        win = VentanaEvento(self)
        if win.run() == Gtk.ResponseType.OK:
            datos = win.recuperar_datos()
            if datos:
                db.CRUD("C", datos)
                self.refrescar()
            else:
                self.alerta("Erro: O campo 'Nome' non pode quedar baleiro.")
        win.destroy()

    def on_ver_resumo(self, _):
        """Abre a Fiestra 3 (Resumo de estatísticas)."""
        total, catering = db.obter_resumo()
        win_resumo = VentanaResumo(total, catering)
        win_resumo.set_transient_for(self)  # Para que quede vinculada á principal
        win_resumo.show()

    def on_del(self, _):
        """Operación crítica con diálogo de confirmación."""
        model, iter = self.tree.get_selection().get_selected()
        if iter:
            confirm = Gtk.MessageDialog(
                transient_for=self,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="¿Estás seguro de que queres eliminar este rexistro?"
            )
            if confirm.run() == Gtk.ResponseType.YES:
                db.CRUD("D", model[iter][0])
                self.refrescar()
            confirm.destroy()
        else:
            self.alerta("Por favor, selecciona primeiro unha fila da táboa.")

    def on_edicion_directa(self, _, path, novo_texto):
        """Actualiza o nome mediante edición directa no TreeView."""
        if novo_texto.strip():
            id_ev = self.store[path][0]
            fila = list(self.store[path][1:])
            fila[0] = novo_texto
            fila.append(id_ev)  # ID para o WHERE do UPDATE
            db.CRUD("U", tuple(fila))
            self.refrescar()

    def alerta(self, texto):
        """Diálogo de aviso para o usuario."""
        msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, texto)
        msg.run()
        msg.destroy()


if __name__ == "__main__":
    win = AppPrincipal()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()