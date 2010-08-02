import gtk

class DiabloDiabetto:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(800, 480)
        window.connect('destroy', self.exit)
        window.show_all()

    def start(self):
        gtk.main()

    def exit(self, event):
        gtk.main_quit()
