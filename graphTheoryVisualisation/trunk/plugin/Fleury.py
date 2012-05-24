#!/usr/bin/python

from connection import connection
import messageWindow
import gobject

class Fleury:

    def __init__(self, paInterface, paButtonMenu, paInitialNode, paSpeed):
        self.__aInterface = paInterface
        self.__aInitialNode = int(paInitialNode)
        self.__aButtonMenu = paButtonMenu
        self.__aSpeed = int(100 - paSpeed)*10
        self.__aNodes = list(self.__aInterface.current_diagram.elements)
        self.__aConnections = []
        self.__aInitialCon = []

        for con in self.__aInterface.current_diagram.connections:
            self.__aConnections.append(connection(con, False))
            if (self.__aConnections[-1].getSource() == self.__aInitialNode) or (self.__aConnections[-1].getDestination() == self.__aInitialNode):
                self.__aInitialCon.append(self.__aConnections[-1])

        self.reset()
        
        for node in self.__aNodes:
            if  len(list(node.connections))%2 != 0 or len(list(node.connections)) == 0:
                del self
                messageWindow.MessageWindow("Fleury algorithm error", "Fleury algorithm can be only runned if all of vertecies \nhave an even degree!")

    def reset(self):
        self.__aEulerianPath = []
        self.__aAllVertices = []
        self.__aConnectedVertices = []
        self.__aSubgraph = list(self.__aConnections)
        self.__aCurentNode = self.__aInitialNode
        self.__aMarkdedCon = 0
        for con in self.__aConnections:
            if con.getConnection().object.values['value'] != "":
                con.getConnection().object.values['value'] = ""
                con.getConnection().object.values['farba'] = "000000"
                con.getConnection().object.values['arrowBegin'] = False
                con.getConnection().object.values['arrowEnd'] = False
                con.setIndex(0)

    def backward(self):
        if self.__aEulerianPath:
            con = self.__aEulerianPath[-1]
            del self.__aEulerianPath[-1]
            con.getConnection().object.values['value'] = ""
            con.getConnection().object.values['farba'] = "000000"
            con.setIndex(0)
            self.__aSubgraph.append(con)
            self.__aMarkdedCon -= 1
            if self.__aCurentNode == con.getSource():
                self.__aCurentNode = con.getDestination()
                con.getConnection().object.values['arrowBegin'] = False
            else:
                self.__aCurentNode = con.getSource()
                con.getConnection().object.values['arrowEnd'] = False

    def play(self):
        for i in range(0,4):
            self.__aButtonMenu[i].enabled = False

        gobject.timeout_add(self.__aSpeed, self.playForward)

    def playForward(self):
        if self.__aSubgraph:
            self.forward()
            return True
        else:
            if not self.__aButtonMenu[0].enabled:
                for i in range(0,4):
                    self.__aButtonMenu[i].enabled = True

    def forward(self):
        if self.__aSubgraph:
            self.step1()

    def step1(self):
        cons = []

        for connection in self.__aSubgraph:
            if (connection.getSource() == self.__aCurentNode) or (connection.getDestination() == self.__aCurentNode):
                cons.append(connection)

        change = self.__aMarkdedCon
        while change == self.__aMarkdedCon:
            con = cons[0]
            del cons[0]
            self.__aSubgraph.remove(con)
            con.setIndex(1)

            self.__aAllVertices = []
            self.__aConnectedVertices = []
            for edge in self.__aSubgraph:
                if edge.getSource() not in self.__aAllVertices:
                    self.__aAllVertices.append(edge.getSource())
                if edge.getDestination() not in self.__aAllVertices:
                    self.__aAllVertices.append(edge.getDestination())

            if self.__aSubgraph:
                self.testConnectivity(self.__aAllVertices[0])
            
            if (len(self.__aAllVertices) == len(self.__aConnectedVertices)) and self.testIsolatedStart(con):
                self.__aEulerianPath.append(con)
                con.getConnection().object.values['farba'] = "FF0000"
                self.__aMarkdedCon += 1
                con.getConnection().object.values['value'] = str(self.__aMarkdedCon)
                if self.__aCurentNode == con.getSource():
                    self.__aCurentNode = con.getDestination()
                    con.getConnection().object.values['farbaEnd'] = "FF0000"
                    con.getConnection().object.values['arrowEnd'] = True
                else:
                    self.__aCurentNode = con.getSource()
                    con.getConnection().object.values['farbaBegin'] = "FF0000"
                    con.getConnection().object.values['arrowBegin'] = True
            else:
                con.setIndex(0)
                self.__aSubgraph.append(con)

    def testIsolatedStart(self, con):
        if (con.getDestination() == self.__aInitialNode or con.getSource() == self.__aInitialNode) and (self.__aCurentNode != self.__aInitialNode):
            count = 0
            for con in self.__aInitialCon:
                if con.getIndex() == 0:
                    count += 1
            if count < 1:
                if self.__aMarkdedCon == len(self.__aConnections) -1:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def testConnectivity(self, vertex):
        for con in self.__aSubgraph:
            if con.getSource() == vertex and con.getDestination() not in self.__aConnectedVertices:
                self.__aConnectedVertices.append(con.getDestination())
                self.testConnectivity(con.getDestination())
            elif con.getDestination() == vertex and con.getSource() not in self.__aConnectedVertices:
                self.__aConnectedVertices.append(con.getSource())
                self.testConnectivity(con.getSource())