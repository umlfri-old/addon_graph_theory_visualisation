#!/usr/bin/python

import gtk
import pango
from threading import Thread

class PyApp(gtk.Window):
    def __init__(self, paData, paAlgorithm):
        super(PyApp, self).__init__()
        self.__aHeader = len(paData)
        self.__aData = paData
        self.__aList = []
        self.__aAlgorithm = paAlgorithm
        self.reset()

    def reset(self):
        if self.__aAlgorithm == "dijkstra" :
            width = self.__aHeader*35
            self.__aColumnSize = 35
        elif self.__aAlgorithm == "kruskal_II":
            width = 80 + self.__aHeader*30
            self.__aColumnSize = 110
        else:
            width = self.__aHeader*30
            self.__aColumnSize = 30

        self.set_size_request(width, 300)
        self.destroy_with_parent
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Result")

        vbox = gtk.VBox(False, 8)

        self.__sw = gtk.ScrolledWindow()
        self.__sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.__sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        vbox.pack_start(self.__sw, True, True, 0)

        self.__aStore = gtk.ListStore(*([str]*(self.__aHeader+1)))

        treeView = gtk.TreeView(self.__aStore)
        treeView.set_property("rules-hint", True)
        self.__sw.add(treeView)
        self.rendererText = gtk.CellRendererText()
        self.rendererText.set_property('xalign', 0.5)
        self.createColumns(treeView)
        self.add(vbox)
        self.set_deletable(False)
        self.show_all()
        self.set_keep_above(True)

    def appendData(self, paData):
        self.__aStore.append(paData + ["white"])
        self.__aList.append(paData)

    def appendColoredData(self, paData):
        self.__aStore.append(paData + ["red"])
        self.__aList.append(paData)
        #self.rendererText.set_property('background', None)

    def deleteData(self):
        self.__aStore.remove(self.__aStore[-1].iter)
        del self.__aList[-1]

    def getLastData(self):
        return self.__aList[-1]

    def createColumns(self, treeView):
        for i in range(0,self.__aHeader):
            column = gtk.TreeViewColumn(self.__aData[i], self.rendererText, text=i, background = self.__aHeader)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
            column.set_fixed_width(self.__aColumnSize)
            if self.__aColumnSize == 110:
                self.__aColumnSize = 30
            column.set_alignment(0.5)
            treeView.append_column(column)

    def clearData(self):
        del self.__aList[:]
        self.__aStore.clear()

    def hide(self):
        self.hide_all()

    def show(self):
        self.show_all()

    def getVisibility(self):
        return self.get_visible()