#!/usr/bin/python
# -*- coding: utf-8 -*-

from basicTarryLabyrint import BasicTarryLabyrint

class Labyrint(BasicTarryLabyrint):
    def __init__(self, paInterface, paButtonMenu, paInitialNode, paSpeed):
        BasicTarryLabyrint.__init__(self, paInterface, paButtonMenu, paInitialNode, paSpeed)
        self.reset()

    def reset(self):
        for con in self._aConnections:
            if con.getConnection().object.values['arrowBegin']:
                con.getConnection().object.values['arrowBegin'] = False
            if con.getConnection().object.values['arrowEnd']:
                con.getConnection().object.values['arrowEnd'] = False
            con.getConnection().object.values['value'] = ""
            if con.getDirectionS_D:
                con.setDirectionS_D(False)
            if con.getDirectionD_S:
                con.setDirectionD_S(False)
        self.__aBackSequence = []
        BasicTarryLabyrint.resetBasic(self)

    def play(self):
        BasicTarryLabyrint.playBasic(self)

    def forward(self):
        BasicTarryLabyrint.forwardBasic(self)

    def backward(self):
        BasicTarryLabyrint.backwardBasic(self)

    def step1(self):
        BasicTarryLabyrint.step1Part1(self)

        if self.priority1UnusedConnection():
            if not self._aBestCon.getTarget() in self._aSequence:
                self._aFirstEdge.append(self._aBestCon.getConnection())
                self._aFirstEdgeAppend = True
        elif not self.priority2ConnectionUsedOnce():
            self.priority3FirstEdge()

        if self._aBestCon:
            if self._aBestCon.getTarget() == self._aBestCon.getSource():
                self._aBestCon.setDirectionD_S(True)
                if self._aFirstEdgeAppend:
                    self.markEdge("=")
                    self._aData[1 + self._aLenCon + self._aBestCon.getTarget()] = "•"
                else:
                    if self._aBestCon.getDirectionS_D():
                        self.__aBackSequence.append(self._aBestCon)
                        self.markEdge("-", 'farbaBegin', "FF0000")
                        self._aBestCon.getConnection().object.values['arrowBegin'] = "True"
                        self._aBestCon.getConnection().object.values['value'] = len(self.__aBackSequence)
                    else:
                        self.markEdge("-")

            else:
                self._aBestCon.setDirectionS_D(True)
                if self._aFirstEdgeAppend:
                    self.markEdge("=")
                    self._aData[1 + self._aLenCon + self._aBestCon.getTarget()] = "•"
                else:
                    if self._aBestCon.getDirectionD_S():
                        self.__aBackSequence.append(self._aBestCon)
                        self.markEdge("-", 'farbaEnd', "FF0000")
                        self._aBestCon.getConnection().object.values['arrowEnd'] = "True"
                        self._aBestCon.getConnection().object.values['value'] = len(self.__aBackSequence)
                    else:
                        self.markEdge("-")
            BasicTarryLabyrint.step1Part2(self)
            if self.__aBackSequence:
                if self._aBestCon == self.__aBackSequence[-1]:
                    self._aList.appendColoredData(self._aData)
                else:
                    self._aList.appendData(self._aData)
            else:
                self._aList.appendData(self._aData)
            BasicTarryLabyrint.step1Part3(self)
        else:
            self._aEnd = True

    def step1back(self):
        BasicTarryLabyrint.step1backPart1(self)
        connection = self._aUsedConnection[-1]
        target = self._aSequence[-1]

        if target == connection.getSource():
            connection.getConnection().object.values['arrowBegin'] = False
            connection.setDirectionD_S(False)
        else:
            connection.getConnection().object.values['arrowEnd'] = False
            connection.setDirectionS_D(False)

        if connection.getConnection() == self._aFirstEdge[-1]:
            del self._aFirstEdge[-1]
            
        if self.__aBackSequence:
            if connection == self.__aBackSequence[-1]:
                self.__aBackSequence[-1].getConnection().object.values['value'] = ""
                del self.__aBackSequence[-1]

        BasicTarryLabyrint.step1backPart2(self)

    def priority1UnusedConnection(self):
        for con in self._aPossibleConnections:
            if (con.getDirectionD_S() == False and con.getDirectionS_D() == False and\
               (float(con.getTarget()) < self._aLowestNode)):
                self._aBestCon = con
                self._aLowestNode = con.getTarget()
        if self._aBestCon:
            return True
        else:
            return False

    def priority2ConnectionUsedOnce(self):
        for con in self._aPossibleConnections:
            if ((con.getDirectionD_S() != con.getDirectionS_D()) and\
               (float(con.getTarget()) < self._aLowestNode) and (con.getConnection() not in self._aFirstEdge)):
                self._aBestCon = con
                self._aLowestNode = con.getTarget()
        if self._aBestCon:
            return True
        else:
            return False

    def priority3FirstEdge(self):
        for con in self._aPossibleConnections:
            if (con.getConnection() in self._aFirstEdge) and (float(con.getTarget()) < self._aLowestNode):
                self._aBestCon = con
                self._aLowestNode = con.getTarget()

    def toggleList(self):
        BasicTarryLabyrint.toggleList(self)

    def getToggleListVisibility(self):
        return self._aList.getVisibility()