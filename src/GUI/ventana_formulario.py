import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class VentanaFormulario(Gtk.Dialog):
    """
    Ventana de diálogo para la gestión de datos de eventos.

    Esta clase implementa un formulario dinámico que permite tanto la creación
    de nuevos registros como la edición de los existentes mediante la precarga
    de datos en sus campos.
    """

    def __init__(self, parent, fila=None):
        """
        Inicializa el formulario de eventos.

        :param parent: Ventana principal que lanza el diálogo.
        :param fila: Lista de datos del evento (opcional) para modo edición.
        """
        titulo = "Editar Evento" if fila else "Nuevo Evento"
        super().__init__(title=titulo, transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(400, 450)

        self.id_evento = fila[0] if fila else None
        area = self.get_content_area()
        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=20)
        area.add(grid)

        # Campos del formulario
        grid.attach(Gtk.Label(label="Nombre:"), 0, 0, 1, 1)
        self.ent_nome = Gtk.Entry(text=fila[1] if fila else "")
        grid.attach(self.ent_nome, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Tipo:"), 0, 1, 1, 1)
        self.cb_tipo = Gtk.ComboBoxText()
        tipos = ["Concierto", "Boda", "Cena", "Otro"]
        for t in tipos: self.cb_tipo.append_text(t)

        if fila and fila[2] in tipos:
            self.cb_tipo.set_active(tipos.index(fila[2]))
        else:
            self.cb_tipo.set_active(0)
        grid.attach(self.cb_tipo, 1, 1, 1, 1)

        self.chk_cat = Gtk.CheckButton(label="Incluir Servicio Catering", active=bool(fila[3]) if fila else False)
        grid.attach(self.chk_cat, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="Prioridad:"), 0, 3, 1, 1)
        self.rb1 = Gtk.RadioButton.new_with_label(None, "Alta")
        self.rb2 = Gtk.RadioButton.new_with_label_from_widget(self.rb1, "Baja")
        if fila and fila[4] == "Baja":
            self.rb2.set_active(True)
        grid.attach(self.rb1, 1, 3, 1, 1)
        grid.attach(self.rb2, 1, 4, 1, 1)

        grid.attach(Gtk.Label(label="Notas adicionales:"), 0, 5, 1, 1)
        self.buffer = Gtk.TextBuffer()
        if fila: self.buffer.set_text(str(fila[5]))
        self.txt_view = Gtk.TextView(buffer=self.buffer, height_request=80)
        grid.attach(self.txt_view, 1, 5, 1, 1)

        self.show_all()

    def recuperar_datos(self):
        """
        Valida y recolecta los datos introducidos en los widgets.

        :return: Tupla con los datos del evento o None si el nombre está vacío.
        """
        nome = self.ent_nome.get_text().strip()
        if not nome: return None

        prio = "Alta" if self.rb1.get_active() else "Baja"
        start, end = self.buffer.get_bounds()
        notas = self.buffer.get_text(start, end, True)

        datos = (nome, self.cb_tipo.get_active_text(), int(self.chk_cat.get_active()), prio, notas)
        if self.id_evento:
            datos += (self.id_evento,)

        return datos