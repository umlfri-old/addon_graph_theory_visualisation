#!/usr/bin/python

from connection import connection

class tarry:

    def __init__(self, paInterface, paInitialNode):
        self.aInterface = paInterface
        self.aCurrentNode = paInitialNode
        self.aStep1 = False

    def step1(self):
        self.aConnections1 = list(self.aInterface.current_diagram.connections)
        self.aConnections = []*len(self.aConnections1)
        self.aEnd = False
        for con in self.aConnections1:
            self.aConnections.append(connection(con))   
        self.aNodes = list(self.aInterface.current_diagram.elements)
        self.aSequence = []*(len(self.aNodes)*2)
        self.aSequence.append(self.aCurrentNode)
        self.aFirstEdge = []*(len(self.aNodes) - 1)
        self.aUsedConnection = []*(len(self.aConnections) + 1)
        self.aPossibleConnections = []*len(self.aConnections)
        self.aLowestNode = float("inf")
        self.aBestCon = None
        self.aStep1 = True


    def play(self):
        self.step1()
        while not self.aEnd:
            self.step2()

    def forward(self):
        if not self.aStep1:
            self.step1()

        if not self.aEnd:
            self.step2()

    def backward(self):
        if self.aSequence and self.aUsedConnection:
            self.step2back()
            
    def step2(self):
        self.aFirstEdgeAppend = False
        for con in self.aConnections:
            if (con.returnSource() == self.aCurrentNode or con.returnDestination() == self.aCurrentNode) and\
                (con.returnDirectionS_D() == False or con.returnDirectionD_S() == False):
                if con.returnSource() == self.aCurrentNode:
                    con.setTarget(False)
                    self.aPossibleConnections.append(con)
                else:
                    con.setTarget(True)
                    self.aPossibleConnections.append(con)

        if not self.priority1():
            if self.priority2():
                self.aFirstEdge.append(self.aBestCon.returnConnection())
                self.aFirstEdgeAppend = True
            else:
                self.priority3()

        if self.aBestCon:
            if self.aBestCon.returnTarget() == self.aBestCon.returnSource():
                self.aBestCon.setDirectionD_S(True)
                if self.aFirstEdgeAppend:
                    self.aBestCon.returnConnection().object.values['farbaBegin'] = "#FF0000"
                else:
                    self.aBestCon.returnConnection().object.values['farbaBegin'] = "#0000FF"
                self.aBestCon.returnConnection().object.values['arrowBegin'] = "True"
                self.aBestCon.returnConnection().object.values['valueS'] = len(self.aSequence)
            else:
                self.aBestCon.setDirectionS_D(True)
                if self.aFirstEdgeAppend:
                    self.aBestCon.returnConnection().object.values['farbaEnd'] = "#FF0000"
                else:
                    self.aBestCon.returnConnection().object.values['farbaEnd'] = "#0000FF"
                self.aBestCon.returnConnection().object.values['arrowEnd'] = "True"
                self.aBestCon.returnConnection().object.values['valueD'] = len(self.aSequence)
            self.aCurrentNode = self.aBestCon.returnTarget()
            self.aSequence.append(self.aCurrentNode)
            del self.aPossibleConnections[:]
            self.aUsedConnection.append(self.aBestCon)
            self.aBestCon = None
            self.aLowestNode = float('inf')
        else:
            self.aEnd = True
            print self.aSequence
            print self.aPossibleConnections
            
    def priority1(self):
        for con in self.aPossibleConnections:
            if (con.returnTarget() in self.aSequence) and (con.returnConnection() not in self.aFirstEdge) and\
               (float(con.returnTarget()) < self.aLowestNode):
                self.aBestCon = con
                self.aLowestNode = con.returnTarget()
        if self.aBestCon:
            return True
        else:
            return False

    def priority2(self):
        for con in self.aPossibleConnections:
            if (con.returnTarget() not in self.aSequence) and (con.returnConnection() not in self.aFirstEdge) and\
               (float(con.returnTarget()) < self.aLowestNode):
                self.aBestCon = con
                self.aLowestNode = con.returnTarget()
        if self.aBestCon:
            return True
        else:
            return False

    def priority3(self):
        for con in self.aPossibleConnections:
            if (con.returnTarget() in self.aSequence) and (con.returnConnection() in self.aFirstEdge) and (float(con.returnTarget()) < self.aLowestNode):
                self.aBestCon = con
                self.aLowestNode = con.returnTarget()

    def step2back(self):
        if self.aEnd:
            self.aEnd = False
        connection = self.aUsedConnection[-1]
        target = self.aSequence[-1]

        if target == connection.returnSource():
            if connection.returnConnection().object.values['farbaBegin'] == "#FF0000":
                del self.aFirstEdge[-1]
            connection.returnConnection().object.values['valueS'] = ""
            connection.returnConnection().object.values['arrowBegin'] = False
            connection.setDirectionD_S(False)
        else:
            if connection.returnConnection().object.values['farbaEnd'] == "#FF0000":
                del self.aFirstEdge[-1]
            connection.returnConnection().object.values['valueD'] = ""
            connection.returnConnection().object.values['arrowEnd'] = False
            connection.setDirectionS_D(False)

        del self.aUsedConnection[-1]
        del self.aSequence[-1]
        if self.aSequence:
            self.aCurrentNode = self.aSequence[-1]
