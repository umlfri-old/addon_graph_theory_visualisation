#!/usr/bin/python

class connection:

    def __init__(self, paConnection):
        self.__aConnection = paConnection
        self.__aSource = int(paConnection.object.source.name)
        self.__aDestination = int(paConnection.object.destination.name)
        self.__aDirectionS_D = False
        self.__aDirectionD_S = False
        self.__aTarget = 0

    def returnConnection(self):
        return self.__aConnection

    def returnSource(self):
        return self.__aSource

    def returnDestination(self):
        return self.__aDestination

    def returnDirectionS_D(self):
        return self.__aDirectionS_D

    def returnDirectionD_S(self):
        return self.__aDirectionD_S

    def setDirectionS_D(self, paValue):
        self.__aDirectionS_D = paValue

    def setDirectionD_S(self, paValue):
        self.__aDirectionD_S = paValue

    def setTarget(self, paTarget):
        if paTarget:
            self.__aTarget = self.__aSource
        else:
            self.__aTarget = self.__aDestination

    def returnTarget(self):
        return self.__aTarget