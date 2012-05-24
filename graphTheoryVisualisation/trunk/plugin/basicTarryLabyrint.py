#!/usr/bin/python
# -*- coding: utf-8 -*-

from connection import connection
from list import PyApp
import gobject

class BasicTarryLabyrint:

    def __init__(self, paInterface, paButtonMenu, paInitialNode, paSpeed):
        self._aInterface = paInterface
        self._aButtonMenu = paButtonMenu
        self._aInitialNode = paInitialNode
        self._aSpeed = int(100 - paSpeed)*10
        self._aNodes = list(self._aInterface.current_diagram.elements)
        self._aConnections = []
        for con in self._aInterface.current_diagram.connections:
            self._aConnections.append(connection(con, False))

    #resetBasic resets attributes, dynamically changing during visualisation to their default values.
    def resetBasic(self):
        self._aCurrentNode = self._aInitialNode
        self._aEnd = False
        self._aSequence = []
        self._aSequence.append(self._aCurrentNode)
        self._aFirstEdge = []
        self._aUsedConnection = []
        self._aPossibleConnections = []
        self._aLowestNode = float("inf")
        self._aBestCon = None
        self._aLenCon = len(self._aConnections)
        self._aLenNod = len(list(self._aInterface.current_diagram.elements))
        self._aConnections = sorted(self._aConnections, key = lambda connection: (connection.getLower(), connection.getHigher()))

        try:
            self._aList.clearData()
        except AttributeError:
            self._aData = ["r",""]

            for i in range(0, self._aLenCon):
                self._aData.append("{" + str(self._aConnections[i].getLower()) + "," + str(self._aConnections[i].getHigher()) + "}")
                self._aConnections[i].setIndex(i+2)

            for i in range(1, self._aLenNod + 1):
                self._aData.append(str(i))

            self._aList = PyApp(self._aData, "tarry")

        for i in range(0, len(self._aData)):
            self._aData[i] = ""
        self._aData[0] = "0"
        self._aData[1 + self._aLenCon + self._aCurrentNode] = "•"
        self._aList.appendData(self._aData)
        self._aData[1 + self._aLenCon + self._aCurrentNode] = ""
        self._aStepNo = 1

    #Repeatedly calls method playForwardBasic in constant time intervals. Its creates illusion of playing algorithm.
    def playBasic(self):
        for i in range(0,4):
            self._aButtonMenu[i].enabled = False

        gobject.timeout_add(self._aSpeed, self.playForwardBasic)

    #Method for step forward. Returns true if method forwardBasic was successfully runned.
    def playForwardBasic(self):
        if not self._aEnd:
            self.forwardBasic()
            return True
        else:
            if not self._aButtonMenu[0].enabled:
                for i in range(0,4):
                    self._aButtonMenu[i].enabled = True

    def forwardBasic(self,):
        if not self._aEnd:
            self.step1()

    def backwardBasic(self):
        if self._aSequence and self._aUsedConnection:
            self.step1back()
            self._aList.deleteData()
            self._aStepNo -= 1

    def step1Part1(self):
        self._aFirstEdgeAppend = False
        for con in self._aConnections:
            if (con.getSource() == self._aCurrentNode) and (con.getDirectionS_D() == False):
                con.setTarget("d")
                self._aPossibleConnections.append(con)
            elif (con.getDestination() == self._aCurrentNode) and (con.getDirectionD_S() == False):
                con.setTarget("s")
                self._aPossibleConnections.append(con)



    def step1Part2(self):
        self._aData[1] = "{" + str(self._aCurrentNode) + "," + str(self._aBestCon.getTarget()) + "}"
        self._aCurrentNode = self._aBestCon.getTarget()
        self._aSequence.append(self._aCurrentNode)
        self._aData[0] = str(self._aStepNo)

    def step1Part3(self):
        self._aData[self._aBestCon.getIndex()] = ""
        self._aData[1 + self._aLenCon + self._aBestCon.getTarget()] = ""
        self._aStepNo += 1
        del self._aPossibleConnections[:]
        self._aUsedConnection.append(self._aBestCon)
        self._aBestCon = None
        self._aLowestNode = float('inf')

    #Mark edges according to connection type and others optional parameters.
    def markEdge(self, type, *arg):
        if arg:
            self._aBestCon.getConnection().object.values[arg[0]] = arg[1]
        if self._aBestCon.getLower() == self._aBestCon.getTarget():
            self._aData[self._aBestCon.getIndex()] = "<" + type
        else:
            self._aData[self._aBestCon.getIndex()] = type + ">"

    def step1backPart1(self):
        if self._aEnd:
            self._aEnd = False

    def step1backPart2(self):
        del self._aUsedConnection[-1]
        del self._aSequence[-1]
        if self._aSequence:
            self._aCurrentNode = self._aSequence[-1]

    #Hides or shows data table.
    def toggleList(self):
        if self._aList.getVisibility():
            self._aList.hide()
        else:
            self._aList.show()
