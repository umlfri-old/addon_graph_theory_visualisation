#!/usr/bin/python

from connection import connection
import gobject

class Kruskal_I:
    
    def __init__(self, paInterface, paButtonMenu, paType, paSpeed):
        self.__aInterface = paInterface
        self.__aButtonMenu = paButtonMenu
        self.__aSpeed = int(100 - paSpeed)*10
        self.__aNodes = list(self.__aInterface.current_diagram.elements)
        self.__aConnections = []
        for con in self.__aInterface.current_diagram.connections:
            self.__aConnections.append(connection(con, True))
            
        if paType == "Max":
            self.__aConnections = sorted(self.__aConnections, key = lambda connection: connection.getValue(), reverse = True)
        else:
            self.__aConnections = sorted(self.__aConnections, key = lambda connection: connection.getValue())
        self.__aConnectionsReset = list(self.__aConnections)
        self.reset()

    def reset(self):
        self.__aSkeleton = []
        self.__aSequence = []
        self.__aCycle = False
        self.__aDfs = False
        self.__aChange = False
        self.__aConnections = list(self.__aConnectionsReset)
        for con in self.__aConnections:
            if con.getConnection().object.values['farba'] != "#000000":
                con.getConnection().object.values['farba'] = "#000000"
                con.getConnection().object.values['lineWidth'] = "2"
             
    def step1(self):
        con = self.__aConnections[0]
        del self.__aConnections[0]

        self.__aSkeleton.append(con)

        if (con.getSource() in self.__aSequence) and (con.getDestination() in self.__aSequence):
            self.__aDfs = True

        if con.getSource() not in self.__aSequence:
            self.__aSequence.append(con.getSource())

        if con.getDestination() not in self.__aSequence:
            self.__aSequence.append(con.getDestination())

        self.__aUnexploredVertex = list(self.__aSequence)
        self.__aUnexploredCon = list(self.__aSkeleton)

        if self.__aDfs:
            while self.__aUnexploredVertex:
                self.dfs(self.__aUnexploredVertex[0])
            if self.__aCycle:
                self.__aSkeleton.remove(con)
            self.__aCycle = False
            self.__aDfs = False
            
        if con in self.__aSkeleton:
            con.getConnection().object.values['farba'] = "#FF0000"
            con.getConnection().object.values['lineWidth'] = "4"
            self.__aChange = True

    def dfs(self, vertex):
        self.__aUnexploredVertex.remove(vertex)
        for con in self.__aSkeleton:
            if (con.getSource() == vertex) or (con.getDestination() == vertex):
                if con in self.__aUnexploredCon:
                    if vertex == con.getSource():
                        newVertex = con.getDestination()
                    else:
                        newVertex = con.getSource()

                    if newVertex in self.__aUnexploredVertex:
                        self.__aUnexploredCon.remove(con)
                        self.dfs(newVertex)
                    else:
                        self.__aCycle = True

    def backward(self):
        if self.__aSkeleton:
            dest = False
            sour = False
            con = self.__aSkeleton[-1]
            del self.__aSkeleton[-1]
            for con1 in self.__aSkeleton:
                if con.getDestination() == con1.getDestination() or con.getDestination() == con1.getSource():
                    dest = True
                if con.getSource() == con1.getDestination() or con.getSource() == con1.getSource():
                    sour = True
            if not dest:
                self.__aSequence.remove(con.getDestination())
            if not sour:
                self.__aSequence.remove(con.getSource())
            con.getConnection().object.values['farba'] = "#000000"
            con.getConnection().object.values['lineWidth'] = "2"
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