import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class VentanaEvento(Gtk.Dialog):
    """VENTANA 2: Diálogo para añadir o editar eventos."""

    def __init__(self, parent, fila=None):
        super().__init__(title="Detalles do Evento", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(350, 400)

        # Agrupación con Frame (Requisito de Diseño)
        frame = Gtk.Frame(label=" Formulario de Datos ", margin=10)
        self.get_content_area().add(frame)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=15)
        frame.add(grid)

        # Widgets
        grid.attach(Gtk.Label(label="Nome:"), 0, 0, 1, 1)
        self.ent_nome = Gtk.Entry(text=fila[1] if fila else "")
        grid.attach(self.ent_nome, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Tipo:"), 0, 1, 1, 1)
        self.cb_tipo = Gtk.ComboBoxText()
        for t in ["Concert", "Boda", "Cea", "Outro"]: self.cb_tipo.append_text(t)
        self.cb_tipo.set_active(0)
        grid.attach(self.cb_tipo, 1, 1, 1, 1)

        self.chk_cat = Gtk.CheckButton(label="Incluír Catering", active=bool(fila[3]) if fila else False)
        grid.attach(self.chk_cat, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="Prioridade:"), 0, 3, 1, 1)
        self.rb1 = Gtk.RadioButton.new_with_label(None, "Alta")
        self.rb2 = Gtk.RadioButton.new_with_label_from_widget(self.rb1, "Baixa")
        grid.attach(self.rb1, 1, 3, 1, 1)
        grid.attach(self.rb2, 1, 4, 1, 1)

        # Notas con TextView (Requisito)
        grid.attach(Gtk.Label(label="Notas:"), 0, 5, 1, 1)
        self.buffer = Gtk.TextBuffer()
        if fila: self.buffer.set_text(fila[5])
        self.txt_view = Gtk.TextView(buffer=self.buffer, height_request=80)
        grid.attach(self.txt_view, 1, 5, 1, 1)

        self.show_all()

    def recuperar_datos(self):
        """Valida y devuelve los datos introducidos."""
        nome = self.ent_nome.get_text().strip()
        if not nome: return None

        prio = "Alta" if self.rb1.get_active() else "Baixa"
        start, end = self.buffer.get_bounds()
        notas = self.buffer.get_text(start, end, True)

        return (nome, self.cb_tipo.get_active_text(), int(self.chk_cat.get_active()), prio, notas)


class VentanaResumo(Gtk.Window):
    """VENTANA 3: Ventana independiente de estadísticas."""

    def __init__(self, total, catering):
        super().__init__(title="Estatísticas do Sistema")
        self.set_default_size(300, 200)
        self.set_border_width(20)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)

        # Uso de Gtk.Label con Markup para mejor diseño
        lbl_info = Gtk.Label()
        lbl_info.set_markup(
            f"<span size='large'><b>Resumo do Proxecto</b></span>\n\n"
            f"• Eventos totais: <b>{total}</b>\n"
            f"• Con servizo de catering: <b>{catering}</b>"
        )
        vbox.pack_start(lbl_info, True, True, 0)

        btn_close = Gtk.Button(label="Entendido")
        btn_close.connect("clicked", lambda w: self.destroy())
        vbox.pack_start(btn_close, False, False, 0)

        self.show_all()