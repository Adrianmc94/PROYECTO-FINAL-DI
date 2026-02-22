import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import conexionBD as db
from GUI.ventana_formulario import VentanaFormulario
from GUI.ventana_resumo import VentanaResumo


class AppPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__(title="Xestor de Eventos DAM")
        self.set_default_size(800, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Cargar estilos antes de mostrar los widgets
        self.aplicar_estilos()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=15)
        self.add(vbox)

        # TABLA
        frame_taboa = Gtk.Frame(label=" Eventos Rexistrados ")
        vbox.pack_start(frame_taboa, True, True, 0)

        self.store = Gtk.ListStore(int, str, str, int, str, str)
        self.tree = Gtk.TreeView(model=self.store)

        for i, tit in enumerate(["ID", "Nombre", "Tipo", "Cat.", "Prio.", "Notas"]):
            col = Gtk.TreeViewColumn(tit, Gtk.CellRendererText(), text=i)
            self.tree.append_column(col)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tree)
        frame_taboa.add(scroll)

        # BOTONES
        hbox = Gtk.Box(spacing=10)
        vbox.pack_end(hbox, False, False, 0)

        # Botón Engadir
        self.btn_add = Gtk.Button(label="Añadir")
        self.btn_add.get_style_context().add_class("btn-add")
        self.btn_add.connect("clicked", self.on_add)
        hbox.pack_start(self.btn_add, True, True, 0)

        # Botón Editar
        self.btn_edit = Gtk.Button(label="Editar")
        hbox.pack_start(self.btn_edit, True, True, 0)
        self.btn_edit.connect("clicked", self.on_edit)

        # Botón Estatísticas
        self.btn_resumo = Gtk.Button(label="Estatísticas")
        self.btn_resumo.get_style_context().add_class("btn-stats")  # Clase según tu style.css
        self.btn_resumo.connect("clicked", self.on_ver_resumo)
        hbox.pack_start(self.btn_resumo, True, True, 0)

        # Botón Eliminar
        self.btn_del = Gtk.Button(label="Eliminar")
        self.btn_del.get_style_context().add_class("btn-del")
        self.btn_del.connect("clicked", self.on_del)
        hbox.pack_start(self.btn_del, True, True, 0)

        db.inicializar_bd()
        self.refrescar()
        self.show_all()

    def aplicar_estilos(self):
        """Busca el CSS en la carpeta /assets/ situada en la raíz del proyecto."""
        css_provider = Gtk.CssProvider()

        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_css = os.path.join(os.path.dirname(ruta_base), "assets", "style.css")

        try:
            if os.path.exists(ruta_css):
                css_provider.load_from_path(ruta_css)
                Gtk.StyleContext.add_provider_for_screen(
                    Gdk.Screen.get_default(),
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
                print(f"Estilos cargados desde: {ruta_css}")
            else:
                print(f"Advertencia: No se encontró el CSS en {ruta_css}")
        except Exception as e:
            print(f"Erro ao cargar CSS: {e}")

    def refrescar(self):
        self.store.clear()
        for r in db.CRUD("R"):
            self.store.append(list(r))

    def on_add(self, _):
        win = VentanaFormulario(self)
        if win.run() == Gtk.ResponseType.OK:
            datos = win.recuperar_datos()
            if datos:
                db.CRUD("C", datos)
                self.refrescar()
        win.destroy()

    def on_edit(self, _):
        model, iter = self.tree.get_selection().get_selected()
        if iter:
            fila = list(model[iter])
            win = VentanaFormulario(self, fila=fila)
            if win.run() == Gtk.ResponseType.OK:
                datos = win.recuperar_datos()
                if datos:
                    # El orden de los datos debe coincidir con el UPDATE en conexionBD.py
                    db.CRUD("U", datos)
                    self.refrescar()
            win.destroy()
        else:
            self.alerta("Selecciona un evento para editar.")

    def on_ver_resumo(self, _):
        # Asegúrate de que db.obter_resumo() devuelva los 5 valores necesarios
        total, catering, por_tipo, nomes_catering, nomes_alta = db.obter_resumo()
        win_resumo = VentanaResumo(total, catering, por_tipo, nomes_catering, nomes_alta)
        win_resumo.set_transient_for(self)
        win_resumo.show()

    def on_del(self, _):
        model, iter = self.tree.get_selection().get_selected()
        if iter:
            confirm = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                        Gtk.ButtonsType.YES_NO, "¿Estás seguro?")
            if confirm.run() == Gtk.ResponseType.YES:
                db.CRUD("D", model[iter][0])
                self.refrescar()
            confirm.destroy()
        else:
            self.alerta("Selecciona primero una fila.")

    def alerta(self, msg):
        d = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg)
        d.run()
        d.destroy()


if __name__ == "__main__":
    win = AppPrincipal()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()