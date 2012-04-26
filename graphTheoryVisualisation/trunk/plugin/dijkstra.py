#!/usr/bin/python

from connection import connection
from list import PyApp
import gobject

class Dijkstra():

    def __init__(self, paInterface, paButtonMenu, paInitialNode, paEndNode, paSpeed):
        self.__aEndNode = paEndNode
        self.__aInitialNode = paInitialNode
        self.__aInterface = paInterface
        self.__aButtonMenu = paButtonMenu
        self.__aSpeed = int(100 - paSpeed)*10
        self.__aInf = float("inf")
        self.__aNodes = list(self.__aInterface.current_diagram.elements)
        self.__aConnections = []
        for con in self.__aInterface.current_diagram.connections:
            self.__aConnections.append(connection(con, True))
        self.reset()

    def reset(self):
        self.__aCurrentNode = self.__aInitialNode
        self.__aStep1 = False
        self.__aStep2 = False
        self.__aStep3  = True
        self.__aFinalValue = 0
        self.__aTentativeDistance = []
        self.__aPreviousNode = []
        self.__aVisited = []
        for vertex  in self.__aNodes:
            self.__aTentativeDistance.append(self.__aInf)
            self.__aPreviousNode.append(0)
            self.__aVisited.append(False)
            if vertex.object.values['farba'] != "#FFFFFF":
                vertex.object.values['farba'] = "#FFFFFF"
                vertex.object.values['farbaBorder'] = "#000000"
                vertex.object.values['result'] = ""
        for con in self.__aInterface.current_diagram.connections:
            if con.object.values['farba'] != "#000000":
                con.object.values['farba'] = "#000000"
        self.__aTentativeDistance[self.__aInitialNode - 1] = 0
        self.__aVisited[self.__aInitialNode - 1] = True
        self.__aUnmarkedConnections = list(self.__aConnections)
        self.__aLastUnmarkedConnections = []
        self.__aMarkedConnections = []
        self.__aResultChanges = []
        self.__aDistanceChanges = []
        self.__aShortestConnections = []
        self.__aBlackenedConnections = []
        self.__aColoredNodes = []
        self.__aColoredNodes.append(self.__aInitialNode)
        self.__aSteps = []
        try:
            self.__aList.clearData()
        except AttributeError:
            self.__aData = ["r","x(r)","t(r)",]
            for i in range(1, len(self.__aNodes) + 1):
                self.__aData.append(str(i))
            self.__aList = PyApp(self.__aData, "dijkstra")
        for i in range(0, len(self.__aData)):
            self.__aData[i] = ""
        self.__aData[3] = "t(v)"
        self.__aData[4] = "|"
        self.__aData[5] = "x(v)"
        self.__aList.appendData(self.__aData)

    def step1(self):
        if self.__aNodes[self.__aInitialNode - 1].object.values['farba'] == "#FFFFFF":
            self.__aNodes[self.__aInitialNode - 1].object.values['farba'] = "#FF0000"
            self.__aNodes[self.__aInitialNode - 1].object.values['farbaBorder'] = "#00FF00"
            self.__aNodes[self.__aInitialNode - 1].object.values['result'] = "0|-"
            self.__aSteps.append(1)
            self.__aStep1 = True
            for i in range(0,3):
                self.__aData[i] = "-"

            for i in range(3,len(self.__aData)):
                if i == self.__aCurrentNode + 2:
                    self.__aData[i] = " 0 |   "
                else:
                    self.__aData[i] = "inf|"
            self.__aList.appendData(self.__aData)
            self.__aData[self.__aCurrentNode + 2] = ""
        else:
            self.__aNodes[self.__aInitialNode - 1].object.values['farba'] = "#FFFFFF"
            self.__aNodes[self.__aInitialNode - 1].object.values['farbaBorder'] = "#000000"
            self.__aNodes[self.__aInitialNode - 1].object.values['result'] = ""
            self.__aData = list(self.__aList.getLastData())
            self.__aList.deleteData()
            self.__aStep1 = False

    def step2(self):
        change = False
        while self.__aUnmarkedConnections:
            con = self.__aUnmarkedConnections[0]
            if self.__aCurrentNode == con.getSource():
                if ((self.__aVisited[con.getDestination() - 1] == False) and
                    (self.__aTentativeDistance[con.getDestination() - 1] > (self.__aTentativeDistance[con.getSource() - 1] + float(con.getConnection().object.values['value'])))):
                    self.__aDistanceChanges.append(self.__aTentativeDistance[int(con.getDestination()) - 1])
                    self.__aTentativeDistance[con.getDestination() - 1] = self.__aTentativeDistance[con.getSource() - 1] + float(con.getConnection().object.values['value'])
                    self.__aPreviousNode[con.getDestination() - 1] = self.__aCurrentNode
                    self.__aResultChanges.append(self.__aNodes[con.getDestination() - 1].object.values['result'])
                    self.__aNodes[con.getDestination() - 1].object.values['result'] = str(self.__aTentativeDistance[con.getDestination() - 1]) + "|" + str(self.__aCurrentNode)
                    con.getConnection().object.values['farba'] = "#0000FF"
                    self.__aLastUnmarkedConnections.append(list(self.__aUnmarkedConnections))
                    self.__aData[con.getDestination() + 2] = self.__aNodes[con.getDestination() - 1].object.values['result']
                    self.__aUnmarkedConnections.remove(con)
                    self.__aMarkedConnections.append(con)
                    self.__aSteps.append(2)
                    change = True
                    break
            self.__aUnmarkedConnections.remove(con);

        if not self.__aUnmarkedConnections:
            self.__aStep2 = True
            self.__aStep3 = False
            self.__aUnmarkedConnections = list(self.__aConnections)
            if not change:
                self.step3()

    def step3(self):
        self.__aSteps.append(3)
        self.__aIndexTD = 0
        self.__aValueTD = self.__aInf
        for temporary in self.__aVisited:
            if not temporary:
                if self.__aTentativeDistance[self.__aIndexTD] < self.__aValueTD:
                    self.__aValueTD = self.__aTentativeDistance[self.__aIndexTD]
                    self.__aIndexFinal = self.__aIndexTD
            self.__aIndexTD += 1
        self.__aData[0] = self.__aCurrentNode
        self.__aData[2] = self.__aTentativeDistance[self.__aCurrentNode -1]

        for con in self.__aConnections:
            if self.__aPreviousNode[self.__aIndexFinal] == con.getSource() and self.__aIndexFinal + 1 == con.getDestination():
                con.getConnection().object.values['farba'] = "#00FF00"
                self.__aShortestConnections.append(con)
        if self.__aShortestConnections[-1].getSource() == self.__aInitialNode:
            self.__aData[1] = "-"
        else:
            self.__aData[1] = self.__aShortestConnections[-2].getSource()
        for con in self.__aConnections:
            if self.__aIndexFinal + 1 == con.getDestination() and con.getConnection().object.values['farba'] == "#0000FF":
                con.getConnection().object.values['farba'] = "#000000"
                self.__aBlackenedConnections.append(con)

        self.__aVisited[self.__aIndexFinal] = True
        self.__aNodes[self.__aCurrentNode - 1].object.values['farba'] = "#00FF00"
        self.__aCurrentNode = self.__aIndexFinal + 1
        self.__aColoredNodes.append(self.__aCurrentNode)
        self.__aList.appendData(list(self.__aData))
        self.__aData[self.__aCurrentNode + 2] = ""
        if self.__aCurrentNode != self.__aEndNode:
            self.__aNodes[self.__aCurrentNode - 1].object.values['farba'] = "#FF0000"
            self.__aNodes[self.__aCurrentNode - 1].object.values['farbaBorder'] = "#00FF00"
        else:
            self.__aNodes[self.__aCurrentNode - 1].object.values['farba'] = "#00FF00"
            self.__aNodes[self.__aCurrentNode - 1].object.values['farbaBorder'] = "#00FF00"
            self.__aData[0] = self.__aCurrentNode
            self.__aData[1] = self.__aShortestConnections[-2].getSource()
            self.__aData[2] = self.__aTentativeDistance[self.__aCurrentNode -1]
            for i in range(3,len(self.__aData)):
                self.__aData[i] = ""
            self.__aList.appendData(self.__aData)
        self.__aFinalValue = self.__aTentativeDistance[self.__aIndexFinal]
        self.__aStep3 = True
        self.__aStep2 = False

    def step2back(self):
        lastCon = self.__aMarkedConnections[-1]
        del self.__aMarkedConnections[-1]
        lastResult = self.__aResultChanges[-1]
        del self.__aResultChanges[-1]
        lastDistance = self.__aDistanceChanges[-1]
        del self.__aDistanceChanges[-1]
        self.__aUnmarkedConnections = list(self.__aLastUnmarkedConnections[-1])
        del self.__aLastUnmarkedConnections[-1]
        self.__aTentativeDistance[lastCon.getDestination() - 1] = lastDistance
        self.__aNodes[lastCon.getDestination() - 1].object.values['result'] = lastResult
        lastCon.getConnection().object.values['farba'] = "#000000"
        if self.__aStep2:
            self.__aStep2 = False
        if self.__aSteps[-1] == 3:
            self.__aStep3 = True

    def step3back(self):
        shortestConnection = self.__aShortestConnections[-1]
        del self.__aShortestConnections[-1]
        del self.__aColoredNodes[-1]

        if self.__aCurrentNode == self.__aEndNode:
            self.__aList.deleteData()
            
        self.__aNodes[shortestConnection.getDestination() - 1].object.values['farbaBorder'] = "#000000"
        self.__aNodes[shortestConnection.getDestination() - 1].object.values['farba'] = "#FFFFFF"
        self.__aNodes[self.__aColoredNodes[-1] - 1].object.values['farba'] = "#FF0000"
        self.__aCurrentNode = int(self.__aNodes[self.__aColoredNodes[-1] - 1].object.values['name'])
        shortestConnection.getConnection().object.values['farba'] = "#0000FF"

        if self.__aBlackenedConnections:
            con = self.__aBlackenedConnections[-1]
            while con.getDestination() == shortestConnection.getDestination() and self.__aBlackenedConnections:
                con.getConnection().object.values['farba'] = "#0000FF"
                del self.__aBlackenedConnections[-1]
                if self.__aBlackenedConnections:
                    con = self.__aBlackenedConnections[-1]

        self.__aData = list(self.__aList.getLastData())
        self.__aList.deleteData()
        self.__aVisited[shortestConnection.getDestination() - 1] = False
        self.__aStep2 = True
        self.__aStep3 = False

    def backward(self):
        if self.__aSteps:
            if self.__aSteps[-1] == 1:
                del self.__aSteps[-1]
                self.step1()
            elif self.__aSteps[-1] == 2:
                del self.__aSteps[-1]
                self.step2back()
            elif self.__aSteps[-1] == 3:
                del self.__aSteps[-1]
                self.step3back()

    def play(self):
        for i in range(0,4):
            self.__aButtonMenu[i].enabled = False

        gobject.timeout_add(self.__aSpeed, self.playForward)

    def playForward(self):
        if self.__aCurrentNode != self.__aEndNode:
            self.forward()
            return True
        else:
            if not self.__aButtonMenu[0].enabled:
                for i in range(0,4):
                    self.__aButtonMenu[i].enabled = True

    def forward(self):
        if not self.__aStep1:
            self.step1()
        elif self.__aCurrentNode != self.__aEndNode:
            if not self.__aStep2:
                self.step2()
            elif not self.__aStep3:
                self.step3()

    def toggleList(self):
        if self.__aList.getVisibility():
            self.__aList.hide()
        else:
            self.__aList.show()

    def getToggleListVisibility(self):
        return self.__aList.getVisibility()
 