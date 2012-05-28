#!/usr/bin/python
# -*- coding: utf-8 -*-

from basicTarryLabyrint import BasicTarryLabyrint

class Tarry(BasicTarryLabyrint):
    def __init__(self, paInterface, paButtonMenu, paInitialNode, paSpeed):
        BasicTarryLabyrint.__init__(self, paInterface, paButtonMenu, paInitialNode, paSpeed)
        self.reset()

    def reset(self):
        for con in self._aConnections:
            if con.getConnection().object.values['arrowBegin']:
                con.getConnection().object.values['arrowBegin'] = False
            if con.getConnection().object.values['arrowEnd']:
                con.getConnection().object.values['arrowEnd'] = False
            if con.getConnection().object.values['valueD'] != "":
                con.getConnection().object.values['valueD'] = ""
            if con.getConnection().object.values['valueS'] != "":
                con.getConnection().object.values['valueS'] = ""
            if con.getDirectionS_D:
                con.setDirectionS_D(False)
            if con.getDirectionD_S:
                con.setDirectionD_S(False)
        BasicTarryLabyrint.resetBasic(self)

    def play(self):
        BasicTarryLabyrint.playBasic(self)

    def forward(self):
        BasicTarryLabyrint.forwardBasic(self)

    def backward(self):
        BasicTarryLabyrint.backwardBasic(self)
            
    def step1(self):
        BasicTarryLabyrint.step1Part1(self)

        if not self.priority1():
            if self.priority2():
                self._aFirstEdge.append(self._aBestCon.getConnection())
                self._aFirstEdgeAppend = True
            else:
                self.priority3()

        if self._aBestCon:
            if self._aBestCon.getTarget() == self._aBestCon.getSource():
                self._aBestCon.setDirectionD_S(True)
                if self._aFirstEdgeAppend:
                    self.markEdge("=", 'farbaBegin', "#FF0000")
                    self._aData[1 + self._aLenCon + self._aBestCon.getTarget()] = "•"
                else:
                    self.markEdge("-", 'farbaBegin', "#0000FF")
                self._aBestCon.getConnection().object.values['arrowBegin'] = "True"
                self._aBestCon.getConnection().object.values['valueS'] = len(self._aSequence)

            else:
                self._aBestCon.setDirectionS_D(True)
                if self._aFirstEdgeAppend:
                    self.markEdge("=", 'farbaEnd', "#FF0000",)
                    self._aData[1 + self._aLenCon + self._aBestCon.getTarget()] = "•"
                else:
                    self.markEdge("-", 'farbaEnd', "#0000FF")
                self._aBestCon.getConnection().object.values['arrowEnd'] = "True"
                self._aBestCon.getConnection().object.values['valueD'] = len(self._aSequence)

            BasicTarryLabyrint.step1Part2(self)
            self._aList.appendData(self._aData)
            BasicTarryLabyrint.step1Part3(self)
        else:
            self._aEnd = True

    def step1back(self):
        BasicTarryLabyrint.step1backPart1(self)
        connection = self._aUsedConnection[-1]
        target = self._aSequence[-1]

        if connection.getConnection() == self._aFirstEdge[-1]:
                del self._aFirstEdge[-1]

        if target == connection.getSource():
            connection.getConnection().object.values['valueS'] = ""
            connection.getConnection().object.values['arrowBegin'] = False
            connection.setDirectionD_S(False)
        else:
            connection.getConnection().object.values['valueD'] = ""
            connection.getConnection().object.values['arrowEnd'] = False
            connection.setDirectionS_D(False)

        BasicTarryLabyrint.step1backPart2(self)

    def priority1(self):
        for con in self._aPossibleConnections:
            if (con.getTarget() in self._aSequence) and (con.getConnection() not in self._aFirstEdge) and\
               (float(con.getTarget()) < self._aLowestNode):
                self._aBestCon = con
                self._aLowestNode = con.getTarget()
        if self._aBestCon:
            return True
        else:
            return False

    def priority2(self):
        for con in self._aPossibleConnections:
            if (con.getTarget() not in self._aSequence) and (con.getConnection() not in self._aFirstEdge) and\
               (float(con.getTarget()) < self._aLowestNode):
                self._aBestCon = con
                self._aLowestNode = con.getTarget()
        if self._aBestCon:
            return True
        else:
            return False

    def priority3(self):
        for con in self._aPossibleConnections:
            if (con.getTarget() in self._aSequence) and (con.getConnection() in self._aFirstEdge) and (float(con.getTarget()) < self._aLowestNode):
                self._aBestCon = con
                self._aLowestNode = con.getTarget()


    def toggleList(self):
        BasicTarryLabyrint.toggleList(self)

    def getToggleListVisibility(self):
        return self._aList.getVisibility()