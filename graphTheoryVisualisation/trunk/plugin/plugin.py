#!/usr/bin/python
import dijkstra

class pluginMain:

    def __init__(self, interface):
        self.aInterface = interface
        self.aMenu = self.createMenu()
        self.createButtonMenu()
        interface.add_notification('project-opened', self.showMenu)
        interface.transaction.autocommit = True


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
        submenu.add_menu_item('dijkstra', lambda x:self.chooseAgorithm("dijkstra"), -1, 'Dijkstra')
        return menu

    def createButtonMenu(self):
        self.aButtonMenu = []*3
        self.aButtonMenu.append(self.aInterface.gui_manager.button_bar.add_button('backward', lambda x:self.aAlgorithm.backward(), -1, 'Backward'))
        self.aButtonMenu[0].visible = False
        self.aButtonMenu.append(self.aInterface.gui_manager.button_bar.add_button('play', lambda x:self.aAlgorithm.play(), -1, 'Play'))
        self.aButtonMenu[1].visible = False
        self.aButtonMenu.append(self.aInterface.gui_manager.button_bar.add_button('forward', lambda x:self.aAlgorithm.forward(), -1, 'Forward'))
        self.aButtonMenu[2].visible = False
        
    def premen(self):
        b = 1
        a = self.aInterface.current_diagram.elements
        for bod in a:
            bod.object.values['name'] = b
            b += 1

    def chooseAgorithm(self, paAlgorithm):
        if paAlgorithm == "dijkstra":
            self.aAlgorithm = dijkstra.dijkstra(self.aInterface)
        for button in self.aButtonMenu:
            button.enabled = True