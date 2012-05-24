#!/usr/bin/python

#Class connection is wrapper class for metamodel's connection type.
#It stores its basic values and some additional values for differnt algorithms.

class connection:

    def __init__(self, paConnection, paSetValue):
        self.__aConnection = paConnection
        self.__aSource = int(paConnection.object.source.name)
        self.__aDestination = int(paConnection.object.destination.name)
        self.__aDirectionS_D = False
        self.__aDirectionD_S = False
        if self.__aSource < self.__aDestination:
            self.__aLowerNode = self.__aSource
            self.__aHigherNode = self.__aDestination
        else:
            self.__aLowerNode = self.__aDestination
            self.__aHigherNode = self.__aSource
        if paSetValue:
            self.__aValue = int(self.__aConnection.object.values['value'])
        else:
            self.__aValue = ""
        self.__aTarget = 0
        self.__aIndex = 0

    def getConnection(self):
        return self.__aConnection

    def getValue(self):
        return self.__aValue

    def getSource(self):
        return self.__aSource

    def getDestination(self):
        return self.__aDestination

    def getDirectionS_D(self):
        return self.__aDirectionS_D

    def getDirectionD_S(self):
        return self.__aDirectionD_S

    def setDirectionS_D(self, paValue):
        self.__aDirectionS_D = paValue

    def setDirectionD_S(self, paValue):
        self.__aDirectionD_S = paValue

    def setTarget(self, paTarget):
        if paTarget == "s":
            self.__aTarget = self.__aSource
        else:
            self.__aTarget = self.__aDestination

    def getLower(self):
        return self.__aLowerNode

    def getHigher(self):
        return self.__aHigherNode

    def getTarget(self):
        return self.__aTarget

    def setIndex(self, paIndex):
        self.__aIndex = paIndex

    def getIndex(self):
        return self.__aIndex