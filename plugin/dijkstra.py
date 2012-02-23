#!/usr/bin/python
from basic import basic

class dijkstra(basic):

    def __init__(self, interface, buttonMenu, initialNode, endNode):
        self.aEndNode = endNode
        basic.__init__(self, interface, buttonMenu, initialNode)


    def step1(self):
        self.aFinalValue = 0
        self.aSize = len(self.aNodes)
        self.aTentativeDistance = []*self.aSize
        self.aPreviousNode = []*self.aSize
        self.aVisited = []*self.aSize
        for vertex  in self.aNodes:
            self.aTentativeDistance.append(self.aInf)
            self.aPreviousNode.append(0)
            self.aVisited.append(False)
        self.aTentativeDistance[self.aInitialNode - 1] = 0
        self.aVisited[self.aInitialNode - 1] = True
        self.aUnmarkedConnections = list(self.aConnections)
        self.aLastUnmarkedConnections = []*len(self.aConnections)
        self.aMarkedConnections = []*len(self.aConnections)
        self.aResultChanges = []*len(self.aConnections)
        self.aDistanceChanges = []*len(self.aConnections)
        self.aShortestConnections = []*len(self.aConnections)
        self.aBlackenedConnections = []*len(self.aConnections)
        self.aColoredNodes = []*len(self.aNodes)
        self.aColoredNodes.append(self.aInitialNode)
        self.aSteps = []*(len(self.aConnections)*2)
        if self.aNodes[self.aInitialNode - 1].object.values['farba'] == "#FFFFFF":
            self.aNodes[self.aInitialNode - 1].object.values['farba'] = "#FF0000"
            self.aNodes[self.aInitialNode - 1].object.values['farbaBorder'] = "#00FF00"
            self.aSteps.append(1)
            self.aStep1 = True
        else:
            self.aNodes[self.aInitialNode - 1].object.values['farba'] = "#FFFFFF"
            self.aNodes[self.aInitialNode - 1].object.values['farbaBorder'] = "#000000"
            self.aStep1 = False

    def step2(self):
        change = False
        while self.aUnmarkedConnections:
            con = self.aUnmarkedConnections[0]
            if self.aCurrentNode == int(con.object.source.name):
                if ((self.aVisited[int(con.object.destination.name) - 1] == False) and
                    (self.aTentativeDistance[int(con.object.destination.name) - 1] > (self.aTentativeDistance[int(con.object.source.name) - 1] + float(con.object.values['value'])))):
                    self.aDistanceChanges.append(self.aTentativeDistance[int(con.object.destination.name) - 1])
                    self.aTentativeDistance[int(con.object.destination.name) - 1] = self.aTentativeDistance[int(con.object.source.name) - 1] + float(con.object.values['value'])
                    self.aPreviousNode[int(con.object.destination.name) - 1] = self.aCurrentNode
                    self.aResultChanges.append(self.aNodes[int(con.object.destination.name) - 1].object.values['result'])
                    self.aNodes[int(con.object.destination.name) - 1].object.values['result'] = str(self.aTentativeDistance[int(con.object.destination.name) - 1]) + "|" + str(self.aCurrentNode)
                    con.object.values['farba'] = "#0000FF"
                    self.aLastUnmarkedConnections.append(list(self.aUnmarkedConnections))
                    self.aUnmarkedConnections.remove(con)
                    self.aMarkedConnections.append(con)
                    self.aSteps.append(2)
                    change = True
                    break
            self.aUnmarkedConnections.remove(con);

        if not self.aUnmarkedConnections:
            self.aStep2 = True
            self.aStep3 = False
            self.aUnmarkedConnections = list(self.aConnections)
            if not change:
                self.step3()

    def step3(self):
        self.aSteps.append(3)
        self.aIndexTD = 0
        self.aValueTD = self.aInf
        for temporary in self.aVisited:
            if not temporary:
                if self.aTentativeDistance[self.aIndexTD] < self.aValueTD:
                    self.aValueTD = self.aTentativeDistance[self.aIndexTD]
                    self.aIndexFinal = self.aIndexTD
            self.aIndexTD += 1

        for con in self.aConnections:
            if self.aPreviousNode[self.aIndexFinal] == int(con.object.source.name) and self.aIndexFinal + 1 == int(con.object.destination.name):
                con.object.values['farba'] = "#00FF00"
                self.aShortestConnections.append(con)

        for con in self.aConnections:
            if self.aIndexFinal + 1 == int(con.object.destination.name) and con.object.values['farba'] == "#0000FF":
                con.object.values['farba'] = "#000000"
                self.aBlackenedConnections.append(con)

        self.aVisited[self.aIndexFinal] = True
        self.aNodes[self.aCurrentNode - 1].object.values['farba'] = "#00FF00"
        self.aCurrentNode = self.aIndexFinal + 1
        self.aColoredNodes.append(self.aCurrentNode)
        if self.aCurrentNode != self.aEndNode:
            self.aNodes[self.aCurrentNode - 1].object.values['farba'] = "#FF0000"
            self.aNodes[self.aCurrentNode - 1].object.values['farbaBorder'] = "#00FF00"
        else:
            self.aNodes[self.aCurrentNode - 1].object.values['farba'] = "#00FF00"
            self.aNodes[self.aCurrentNode - 1].object.values['farbaBorder'] = "#00FF00"
        self.aFinalValue = self.aTentativeDistance[self.aIndexFinal]
        self.aStep3 = True
        self.aStep2 = False

    def step2back(self):
        lastCon = self.aMarkedConnections[-1]
        del self.aMarkedConnections[-1]
        lastResult = self.aResultChanges[-1]
        del self.aResultChanges[-1]
        lastDistance = self.aDistanceChanges[-1]
        del self.aDistanceChanges[-1]
        self.aUnmarkedConnections = list(self.aLastUnmarkedConnections[-1])
        del self.aLastUnmarkedConnections[-1]
        self.aTentativeDistance[int(lastCon.object.destination.name) - 1] = lastDistance
        self.aNodes[int(lastCon.object.destination.name) - 1].object.values['result'] = lastResult
        lastCon.object.values['farba'] = "#000000"
        if self.aStep2:
            self.aStep2 = False
        if self.aSteps[-1] == 3:
            self.aStep3 = True

    def step3back(self):
        shortestConnection = self.aShortestConnections[-1]
        del self.aShortestConnections[-1]
        del self.aColoredNodes[-1]
        self.aNodes[int(shortestConnection.object.destination.name) - 1].object.values['farbaBorder'] = "#000000"
        self.aNodes[int(shortestConnection.object.destination.name) - 1].object.values['farba'] = "#FFFFFF"
        self.aNodes[self.aColoredNodes[-1] - 1].object.values['farba'] = "#FF0000"
        self.aCurrentNode = int(self.aNodes[self.aColoredNodes[-1] - 1].object.values['name'])
        shortestConnection.object.values['farba'] = "#0000FF"
        if self.aBlackenedConnections:
            con = self.aBlackenedConnections[-1]
            while con.object.destination.name == shortestConnection.object.destination.name and self.aBlackenedConnections:
                con.object.values['farba'] = "#0000FF"
                del self.aBlackenedConnections[-1]
                if self.aBlackenedConnections:
                    con = self.aBlackenedConnections[-1]
                
        self.aVisited[int(shortestConnection.object.destination.name) - 1] = False
        self.aStep2 = True
        self.aStep3 = False

    def backward(self):
        if self.aSteps[-1] == 1:
            self.step1()
        elif self.aSteps[-1] == 2:
            del self.aSteps[-1]
            self.step2back()
        elif self.aSteps[-1] == 3:
            del self.aSteps[-1]
            self.step3back()

    def forward(self):
        if not self.aStep1:
            self.step1()

        elif self.aCurrentNode != self.aEndNode:
            if not self.aStep2:
                self.step2()
            elif not self.aStep3:
                self.step3()
        else:
            print self.aFinalValue
            print self.aPreviousNode
            print self.aTentativeDistance

    def play(self):
        basic.play(self)
        print self.aFinalValue
        print self.aPreviousNode
        print self.aTentativeDistance
        print self.aStep2
        print self.aStep3