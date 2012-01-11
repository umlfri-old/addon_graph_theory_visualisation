#!/usr/bin/python

class tarry:

    def __init__(self, interface):
        self.aInterface = interface

    def play(self):
        self.aNodes = list(self.aInterface.current.diagram.elements)
        self.aConnections = list(self.aInterface.current_diagram.connection)
        self.aCurrentNode = self.aNodes[0]
        self.aSequence = []*(len(self.aConnections)*2)
        self.aSequence.append(self.aCurrentNode)
        self.aDirectionU_V = []*len(self.aConnections)
        self.aDirectionV_U = []*len(self.aConnections)
        self.aFirstEdge = []*len(self.aConnections)
        for con in self.aConnections:
            self.aDirectionU_V.append(False)
            self.aDirectionV_U.append(False)
        index = 0
        self.aPossibleConnections = []*len(self.aConnections)
        self.aLowestNode = float("inf")

        for con in self.aConnections:
            if con.object.source.name == self.aCurrentNode:
                if not self.aDirectionU_V[index]:
                    self.aPossibleConnections.append(con)
                    self.aDirectionU_V[index] = True
            index += 1
        index = 0

        if self.aPossibleConnections:
            for con in self.aPossibleConnections:
                if float(con.object.destination.name) < self.aLowestNode:
                    self.aLowestNode = float(con.object.destination.name)
                    self.aCurrentNode = con.object.destination.name

            if self.aCurrentNode not in self.aSequence:
                self.aFirstEdge.append(self.aCurrentNode)
            self.aSequence.append(self.aCurrentNode)
            self.aPossibleConnections.clear()

        else:
            for con in self.aConnections:
                if con.object.source.name == self.aCurrentNode:
                    if not self.aDirectionV_U[index]:
                        self.aPossibleConnections.append(con)
                        self.aDirectionV_U[index] = True


            
                
                