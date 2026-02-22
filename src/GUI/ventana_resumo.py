import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class VentanaResumo(Gtk.Window):
    """
    Dashboard de estadísticas y análisis de datos de la aplicación.

    Esta ventana proporciona una vista resumida de la base de datos,
    incluyendo porcentajes de servicios y listados filtrados por prioridad.
    """

    def __init__(self, total, catering, por_tipo, nomes_catering, nomes_alta):
        """
        Inicializa el panel de estadísticas con datos precalculados.
        """
        super().__init__(title="Panel de Control y Estadísticas")
        self.set_default_size(600, 500)
        self.set_border_width(15)

        hbox_principal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.add(hbox_principal)

        # Columna Izquierda: Métricas generales
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        hbox_principal.pack_start(vbox_left, True, True, 0)

        lbl_tit = Gtk.Label()
        lbl_tit.set_markup("<span size='x-large' weight='bold'>Métricas Generales</span>")
        vbox_left.pack_start(lbl_tit, False, False, 0)

        porcentaxe = (catering / total * 100) if total > 0 else 0
        vbox_left.pack_start(Gtk.Label(label=f"Eventos con Catering: {porcentaxe:.1f}%"), False, False, 0)
        progress = Gtk.ProgressBar()
        progress.set_fraction(porcentaxe / 100)
        vbox_left.pack_start(progress, False, False, 0)

        vbox_left.pack_start(Gtk.Label(label="Distribución por Categoría:"), False, False, 5)
        frame_tipo = Gtk.Frame()
        vbox_left.pack_start(frame_tipo, True, True, 0)

        list_tipo = Gtk.ListBox()
        frame_tipo.add(list_tipo)
        for t, c in por_tipo:
            list_tipo.add(Gtk.Label(label=f"{t}: {c} eventos", xalign=0, margin=5))

        # Columna Derecha: Listados específicos
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hbox_principal.pack_start(vbox_right, True, True, 0)

        lbl_prio = Gtk.Label()
        lbl_prio.set_markup("<span foreground='#e74c3c' weight='bold'>Urgente: Prioridad Alta</span>")
        vbox_right.pack_start(lbl_prio, False, False, 0)

        scroll_prio = Gtk.ScrolledWindow(height_request=150)
        vbox_right.pack_start(scroll_prio, True, True, 0)
        list_prio = Gtk.ListBox()
        scroll_prio.add(list_prio)
        for n in nomes_alta:
            list_prio.add(Gtk.Label(label=f"• {n[0]}", xalign=0, margin=5))

        lbl_cat = Gtk.Label()
        lbl_cat.set_markup("<span foreground='#3498db' weight='bold'>Eventos con Catering</span>")
        vbox_right.pack_start(lbl_cat, False, False, 0)

        scroll_cat = Gtk.ScrolledWindow(height_request=150)
        vbox_right.pack_start(scroll_cat, True, True, 0)
        list_cat = Gtk.ListBox()
        scroll_cat.add(list_cat)
        for n in nomes_catering:
            list_cat.add(Gtk.Label(label=f"• {n[0]}", xalign=0, margin=5))

        self.show_all()