#!/usr/bin/python
import gtk
import messageWindow
import os.path

class Window:
    def __init__(self, paPlugin, paInterface):
        self.__aInterface = paInterface
        self.__aPlugin = paPlugin
        builder = gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname(__file__), 'ParameterWindow.glade'))
        self.__aWindow = builder.get_object('window1')
        self.__aOk = builder.get_object('button1')
        self.__aOk.connect('clicked', lambda x:self.ok())
        self.__aCancel = builder.get_object('button2')
        self.__aCancel.connect('clicked', lambda x:self.cancel())
        self.__aCombobox1 = builder.get_object("combobox1")
        self.__aCombobox2 = builder.get_object("combobox2")
        self.__aScale = builder.get_object('hscale1')
        self.__aScale.set_adjustment(gtk.Adjustment(0,0,100,1,0,0))
        self.__aLabel1 = builder.get_object('label1')
        self.__aLabel2 = builder.get_object('label2')
        self.__aModel = None
        self.__aModel1 = gtk.ListStore(str)
        self.__aModel1.append(["Min"])
        self.__aModel1.append(["Max"])
        self.__aElementsNo = 0
        self.__aAlgorithmName = ""

    def setComboModel(self):
        if self.__aAlgorithmName == "Dijkstra":
            self.__aCombobox1.set_model(self.__aModel)
            self.__aCombobox2.set_model(self.__aModel)
        elif self.__aAlgorithmName == "Tarry" or self.__aAlgorithmName == "Fleury" or self.__aAlgorithmName == "Labyrint":
            self.__aCombobox1.set_model(self.__aModel)
        elif self.__aAlgorithmName == "Kruskal_I" or self.__aAlgorithmName == "Kruskal_II":
            self.__aCombobox1.set_model(self.__aModel1)

    def createList(self):
        self.__aModel = gtk.ListStore(str)
        self.__aElementsNo = len(list(self.__aInterface.current_diagram.elements))
        for vertex in self.__aInterface.current_diagram.elements:
            self.__aModel.append([vertex.object.values['name']])

    def renderCombo(self):
        cell = gtk.CellRendererText()
        self.__aCombobox1.pack_start(cell, False)
        self.__aCombobox1.add_attribute(cell, 'text',0)
        self.__aCombobox2.pack_start(cell, False)
        self.__aCombobox2.add_attribute(cell, 'text',0)

    def chooseAlgorithm(self, paAlgorithmName):
        self.__aAlgorithmName = paAlgorithmName
        self.__aWindow.set_title(self.__aAlgorithmName)
        if self.__aElementsNo != len(list(self.__aInterface.current_diagram.elements)):
            self.createList()
            if not self.__aCombobox1.get_cells():
                self.renderCombo()
        self.setComboModel()

        if self.__aAlgorithmName == "Dijkstra":
            self.__aLabel1.set_text("Initial Node:")
            self.__aWindow.show_all()

        elif self.__aAlgorithmName == "Tarry" or self.__aAlgorithmName ==  "Fleury" or self.__aAlgorithmName ==  "Labyrint":
            self.__aLabel1.set_text("Initial Node:")
            self.__aLabel2.hide()
            self.__aCombobox2.hide()
            self.__aWindow.show()

        elif self.__aAlgorithmName == "Kruskal_I" or self.__aAlgorithmName ==  "Kruskal_II":
            self.__aLabel1.set_text("Spanning Tree:")
            self.__aLabel2.hide()
            self.__aCombobox2.hide()
            self.__aWindow.show()

        self.__aWindow.set_keep_above(True)

    def cancel(self):
        self.__aWindow.hide()

    def checkEntry(self,):
        index1 = self.__aCombobox1.get_active()
        index2 = self.__aCombobox2.get_active()
        if index1 != -1:
            self.__aEntry1 = self.__aCombobox1.get_active_text()
            if self.__aAlgorithmName == "Dijkstra":
                if index2 != -1 != "":
                    self.__aEntry2 = self.__aCombobox2.get_active_text()
                    return True
                else:
                    return False
            return True
        else:
            return False

    def ok(self):
        if self.checkEntry():
            self.__aPlugin.ok()
            self.__aWindow.hide()
        else:
            messageWindow.MessageWindow("Value error", "All fields must be filled!")


    def getEntry1(self):
        return self.__aEntry1

    def getEntry2(self):
        return self.__aEntry2

    def getScaleValue(self):
        return self.__aScale.get_value()