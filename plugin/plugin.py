#!/usr/bin/python
import dijkstra
import tarry
import gtk
from org.umlfri.api.mainLoops import GtkMainLoop

class pluginMain:

    def __init__(self, interface):
        self.aInterface = interface
        self.aMenu = self.createMenu()
        self.createButtonMenu()
        interface.add_notification('project-opened', self.showMenu)
        builder = gtk.Builder()
        builder.add_from_file('c:\\loki\\ParameterWindow.glade')
        self.aWindow = builder.get_object('dialog1')
        self.aWindow.connect('delete_event', lambda x, y:self.hideX())
        self.aOk = builder.get_object('button1')
        self.aOk.connect('clicked', lambda x:self.ok())
        self.aCancel = builder.get_object('button2')
        self.aCancel.connect('clicked', lambda x:self.cancel())
        self.aEntry1 = builder.get_object('entry1')
        self.aEntry2 = builder.get_object('entry2')
        self.aEntry3 = builder.get_object('entry3')
        interface.transaction.autocommit = True
        interface.set_main_loop(GtkMainLoop())


    def showMenu(self, *arg):
        if self.aInterface.project.metamodel.uri == "urn:umlfri.org:metamodel:graphTheoryVisualisation":
            self.aMenu.visible = True
            for button in self.aButtonMenu:
                button.visible = True
                button.enabled = False
        else:
            self.aMenu.visible = False

    def createMenu(self):
        menu = self.aInterface.gui_manager.main_menu.add_menu_item('graphMenu', '', -1, 'Algorithm')
        menu.visible = False
        menu.add_submenu()
        submenu = menu.submenu
        submenu.add_menu_item('dijkstra', lambda x:self.chooseAlgorithm("dijkstra"), -1, 'Dijkstra')
        submenu.add_menu_item('tarry', lambda x:self.chooseAlgorithm("tarry"), -1, 'Tarry')
        submenu.add_menu_item('premenuj', lambda x:self.premenuj(), -1, 'Premenuj')
        return menu

    def createButtonMenu(self):
        self.aButtonMenu = []*3
        self.aButtonMenu.append(self.aInterface.gui_manager.button_bar.add_button('backward', lambda x:self.aAlgorithm.backward(), -1, 'Backward'))
        self.aButtonMenu[0].visible = False
        self.aButtonMenu.append(self.aInterface.gui_manager.button_bar.add_button('play', lambda x:self.aAlgorithm.play(), -1, 'Play'))
        self.aButtonMenu[1].visible = False
        self.aButtonMenu.append(self.aInterface.gui_manager.button_bar.add_button('forward', lambda x:self.aAlgorithm.forward(), -1, 'Forward'))
        self.aButtonMenu[2].visible = False
        
    def premenuj(self):
        b = 1
        a = self.aInterface.current_diagram.elements
        for bod in a:
            if bod.object.values['name'] != b:
                bod.object.values['name'] = b
            b += 1

    def chooseAlgorithm(self, paAlgorithm):
        self.aWindow.show_all()
        self.aWindow.set_keep_above(True)
        self.aAlgorithmName = paAlgorithm

    def cancel(self):
        self.aWindow.hide()
        
    def ok(self):
        if self.checkEntry():
            if self.aAlgorithmName == "dijkstra":
                self.aAlgorithm = dijkstra.dijkstra(self.aInterface, self.aButtonMenu, int(self.aEntry1.get_text()),
                                                    int(self.aEntry2.get_text()))
            elif self.aAlgorithmName == "tarry":
                self.aAlgorithm = tarry.tarry(self.aInterface, int(self.aEntry1.get_text()))

            for button in self.aButtonMenu:
                button.enabled = True
            self.aWindow.hide()

    def checkEntry(self):
        try:
            int(self.aEntry1.get_text())
            if self.aAlgorithmName == "dijkstra":
                int(self.aEntry2.get_text())
            return True
        except ValueError:
            return False

    def hideX(self):
        self.aWindow.hide()
        return gtk.TRUE