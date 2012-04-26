#!/usr/bin/python

import dijkstra
import kruskal_I
import kruskal_II
import tarry
import window
import messegeWindow
import fleury
import labyrint
import fileManager
import os.path
from org.umlfri.api.mainLoops import GtkMainLoop

class pluginMain:

    def __init__(self, interface):
        self.__aInterface = interface
        self.__aMenu = None
        self.__aInterface.add_notification('project-opened', self.createUI)
        self.__aAlgorithmName = ""
        self.__aAlgorithm = None
        self.__aInterface.transaction.autocommit = True
        self.__aInterface.set_main_loop(GtkMainLoop())
        self.__aManager = fileManager.FileManager(self.__aInterface)
        self.__aWindow = None

    def createUI(self, *arg):
        if self.__aInterface.project.metamodel.uri == "urn:umlfri.org:metamodel:graphTheoryVisualisation":
            if not self.__aMenu:
                self.__aMenu = self.createMenu()
                self.createButtonMenu()
                self.__aInterface.add_notification('add-element', self.rename)
            self.__aMenu.visible = True
            for button in self.__aButtonMenu:
                button.visible = True
                button.enabled = False
            self.__aButtonMenu[5].enabled = True
            if self.__aAlgorithm:
                try:
                    if self.__aAlgorithm.getToggleListVisibility():
                        self.__aAlgorithm.toggleList()
                except AttributeError:
                    pass
                self.__aAlgorithm = None
        else:
            for button in self.__aButtonMenu:
                button.visible = False
            self.__aMenu.visible = False
            if self.__aAlgorithm:
                try:
                    if self.__aAlgorithm.getToggleListVisibility():
                        self.__aAlgorithm.toggleList()
                except AttributeError:
                    pass

    def createMenu(self):
        menu = self.__aInterface.gui_manager.main_menu.add_menu_item('graphMenu', '', -1, 'Algorithm')
        menu.visible = False
        menu.add_submenu()
        submenu = menu.submenu
        submenu.add_menu_item('dijkstra', lambda x:self.chooseAlgorithm("Dijkstra"), -1, 'Dijkstra')
        submenu.add_menu_item('tarry', lambda x:self.chooseAlgorithm("Tarry"), -1, 'Tarry')
        submenu.add_menu_item('kruskal I', lambda x:self.chooseAlgorithm("Kruskal_I"), -1, 'Kruskal I')
        submenu.add_menu_item('kruskal II', lambda x:self.chooseAlgorithm("Kruskal_II"), -1, 'Kruskal II')
        submenu.add_menu_item('fleury', lambda x:self.chooseAlgorithm("Fleury"), -1, 'Fleury')
        submenu.add_menu_item('labyrint', lambda x:self.chooseAlgorithm("Labyrint"), -1, 'Labyrint')
        return menu

    def createButtonMenu(self):
        self.__aButtonMenu = []
        self.__aButtonMenu.append(self.__aInterface.gui_manager.button_bar.add_button('backward', lambda x:self.__aAlgorithm.backward(), -1, 'Backward', imagefilename = os.path.join('icons', 'backward.png')))
        self.__aButtonMenu.append(self.__aInterface.gui_manager.button_bar.add_button('play', lambda x:self.__aAlgorithm.play(), -1, 'Play', imagefilename = os.path.join('icons', 'play.png')))
        self.__aButtonMenu.append(self.__aInterface.gui_manager.button_bar.add_button('forward', lambda x:self.__aAlgorithm.forward(), -1, 'Forward', imagefilename = os.path.join('icons', 'forward.png')))
        self.__aButtonMenu.append(self.__aInterface.gui_manager.button_bar.add_button('reset', lambda x:self.__aAlgorithm.reset(), -1, 'Reset', imagefilename = os.path.join('icons', 'reset.png')))
        self.__aButtonMenu.append(self.__aInterface.gui_manager.button_bar.add_button('toggle', lambda x:self.__aAlgorithm.toggleList(), -1, 'Toggle List', imagefilename = os.path.join('icons', 'list.png')))
        self.__aButtonMenu.append(self.__aInterface.gui_manager.button_bar.add_button('export', lambda x:self.__aManager.importGraph(), -1, 'Export'))
        for button in self.__aButtonMenu:
            button.visible = False

    def rename(self, *args, **kwds):
        index = 1
        for vertex in self.__aInterface.current_diagram.elements:
            if vertex.object.values['name'] != index:
                vertex.object.values['name'] = index
            index += 1

    def ok(self):
        try:
            self.__aAlgorithm = None
            self.__aCorrection = True
            if self.__aAlgorithmName == "Dijkstra":
                self.checkCorrectSetting("Arc")
                if self.__aCorrection:
                    self.__aAlgorithm = dijkstra.Dijkstra(self.__aInterface, self.__aButtonMenu, int(self.__aWindow.getEntry1()),
                                                      int(self.__aWindow.getEntry2()), float(self.__aWindow.getScaleValue()))
                else:
                    messegeWindow.MessegeWindow("Dijkstra algorithm error", "Dijkstra algorithm can be runned only for diagram \nwhich consist of connection type \'Arc\' with a positive numeric value.")
            elif self.__aAlgorithmName == "Tarry":
                self.checkCorrectSetting("Edge")
                if self.__aCorrection:
                    self.__aAlgorithm = tarry.Tarry(self.__aInterface, self.__aButtonMenu, int(self.__aWindow.getEntry1()), float(self.__aWindow.getScaleValue()))
                else:
                    messegeWindow.MessegeWindow("Tarry algorithm error", "Tarry algorithm can be runned only for diagram \nwhich consist of connection type \'Edge\'.")
            elif self.__aAlgorithmName == "Kruskal_I":
                self.checkCorrectSetting("Edge")
                if self.__aCorrection:
                    self.__aAlgorithm = kruskal_I.Kruskal_I(self.__aInterface, self.__aButtonMenu, self.__aWindow.getEntry1(), float(self.__aWindow.getScaleValue()))
                else:
                    messegeWindow.MessegeWindow("Kruskal I algorithm error", "Kruskal I algorithm can be runned only for diagram \nwhich consist of connection type \'Edge\' with numeric value.")
            elif self.__aAlgorithmName == "Kruskal_II":
                self.checkCorrectSetting("Edge")
                if self.__aCorrection:
                    self.__aAlgorithm = kruskal_II.Kruskal_II(self.__aInterface, self.__aButtonMenu, self.__aWindow.getEntry1(), float(self.__aWindow.getScaleValue()))
                else:
                    messegeWindow.MessegeWindow("Kruskal II algorithm error", "Kruskal II algorithm can be runned only for diagram \nwhich consist of connection type \'Edge\' with numeric value.")
            elif self.__aAlgorithmName == "Fleury":
                self.checkCorrectSetting("Edge")
                if self.__aCorrection:
                    self.__aAlgorithm = fleury.Fleury(self.__aInterface, self.__aButtonMenu, self.__aWindow.getEntry1(), float(self.__aWindow.getScaleValue()))
                else:
                    messegeWindow.MessegeWindow("Fleury algorithm error", "Fleury algorithm can be runned only for diagram \nwhich consist of connection type \'Edge\'.")
            elif self.__aAlgorithmName == "Labyrint":
                self.checkCorrectSetting("Edge")
                if self.__aCorrection:
                    self.__aAlgorithm = labyrint.Labyrint(self.__aInterface, self.__aButtonMenu, int(self.__aWindow.getEntry1()), float(self.__aWindow.getScaleValue()))
                else:
                    messegeWindow.MessegeWindow("Labyrint algorithm error", "Labyrint algorithm can be runned only for diagram \nwhich consist of connection type \'Edge\'.")

            if self.__aAlgorithm:
                for i in range(0,6):
                    self.__aButtonMenu[i].enabled = True
                if self.__aAlgorithmName != "Fleury" and self.__aAlgorithmName != "Kruskal_I":
                    self.__aButtonMenu[4].enabled = True
                else:
                    self.__aButtonMenu[4].enabled = False
            else:
                for button in self.__aButtonMenu:
                    button.enabled = False
        except Exception:
            messegeWindow.MessegeWindow("Diagram error", "Something goes wrong. Please restart plugin.")

    def checkCorrectSetting(self, paTypeCon):
        for con in self.__aInterface.current_diagram.connections:
            if self.__aCorrection:
                if con.object.type.name != paTypeCon:
                    self.__aCorrection = False
                elif self.__aAlgorithmName == "Dijkstra" or self.__aAlgorithmName == "Kruskal_I" or\
                    self.__aAlgorithmName == "Kruskal_II":
                    try:
                        if int(con.object.values['value']) < 0 and self.__aAlgorithmName == "Dijkstra":
                            self.__aCorrection = False
                    except ValueError:
                        self.__aCorrection = False

    def chooseAlgorithm(self, paAlgorithmName):
        self.__aAlgorithmName = paAlgorithmName
        if self.__aAlgorithm:
            try:
                if self.__aAlgorithm.getToggleListVisibility():
                    self.__aAlgorithm.toggleList()
            except AttributeError:
                pass
            self.__aAlgorithm.reset()
        self.__aWindow = window.Window(self, self.__aInterface)
        self.__aWindow.chooseAlgorithm(paAlgorithmName)