#!/usr/bin/python

from connection import connection
from list import PyApp
import gobject

class Kruskal_II:

    def __init__(self, paInterface, paButtonMenu, paType, paSpeed):
        self.__aInterface = paInterface
        self.__aButtonMenu = paButtonMenu
        self.__aSpeed = int(100 - paSpeed)*10
        self.__aNodesValues = []
        self.__aConnections = []

        for con in self.__aInterface.current_diagram.connections:
            self.__aConnections.append(connection(con, True))

        if paType == "Max":
            self.__aConnections = sorted(self.__aConnections, key = lambda connection: connection.getValue(), reverse = True)
        else:
            self.__aConnections = sorted(self.__aConnections, key = lambda connection: connection.getValue())

        self.__aConnectionsReset = list(self.__aConnections)
        index = 1
        for node in self.__aInterface.current_diagram.elements:
            self.__aNodesValues.append(index)
            index += 1

        self.reset()

    def reset(self):
        self.__aChangedValues = []
        self.__aSkeleton = []
        self.__aSequence = []
        self.__aNodes = list(self.__aNodesValues)

        try:
            self.__aList.clearData()
            self.__aConnections = list(self.__aConnectionsReset)
        except AttributeError:
            self.__aData = ["Spanning tree edge"]
            for node in self.__aNodes:
                self.__aData.append(str(node))
            self.__aList = PyApp(self.__aData, "kruskal_II")

        for con in self.__aConnections:
            if con.getConnection().object.values['farba'] != "000000":
                con.getConnection().object.values['farba'] = "000000"
                con.getConnection().object.values['lineWidth'] = "2"
           
        for index in range(2, len(self.__aData)):
            self.__aData[index] = ""
        self.__aData[0] = "-"
        self.__aData[1] = "k(v)"
        self.__aList.appendData(self.__aData)
        self.__aChange = False

    def step1(self):
        con = self.__aConnections[0]
        del self.__aConnections[0]

        if self.__aNodes[con.getLower() - 1] != self.__aNodes[con.getHigher() - 1]:
            self.__aSkeleton.append(con)
            con.getConnection().object.values['farba'] = "FF0000"
            con.getConnection().object.values['lineWidth'] = "4"
            self.__aData[0] = "{" + str(con.getLower()) + "," + str(con.getHigher()) + "}"
            changes = list(self.__aNodes)
            self.__aChange = True
            changingValue = self.__aNodes[con.getHigher() - 1]

            for node in self.__aNodesValues:
                if self.__aNodes[node - 1] == changingValue:
                    changes[node - 1] = self.__aNodes[node - 1]
                    self.__aNodes[node - 1] = self.__aNodes[con.getLower() - 1]
                else:
                    changes[node - 1] = 0
                self.__aData[node] = self.__aNodes[node - 1]

            self.__aChangedValues.append(changes)
            self.__aList.appendData(self.__aData)

    def backward(self):
        if self.__aSkeleton:
            con = self.__aSkeleton[-1]
            del self.__aSkeleton[-1]
            con.getConnection().object.values['farba'] = "#000000"
            con.getConnection().object.values['lineWidth'] = "2"
            changes = self.__aChangedValues[-1]
            del self.__aChangedValues[-1]
            index = 0

            for change in changes:
                if change != 0:
                    self.__aNodes[index] = change
                index += 1

            self.__aList.deleteData()
            self.__aConnections.reverse()
            self.__aConnections.append(con)
            self.__aConnections.reverse()

    def play(self):
        for i in range(0,4):
            self.__aButtonMenu[i].enabled = False

        gobject.timeout_add(self.__aSpeed, self.playForward)

    def playForward(self):
        if self.__aConnections and (len(self.__aSkeleton) != (len(self.__aNodes) - 1)):
            self.forward()
            return True
        else:
            if not self.__aButtonMenu[0].enabled:
                for i in range(0,4):
                    self.__aButtonMenu[i].enabled = True


    def forward(self):
        if self.__aConnections and (len(self.__aSkeleton) != (len(self.__aNodes) - 1)):
            while not self.__aChange:
                self.step1()
            self.__aChange = False

    def toggleList(self):
        if self.__aList.getVisibility():
            self.__aList.hide()
        else:
            self.__aList.show()

    def getToggleListVisibility(self):
        return self.__aList.getVisibility()