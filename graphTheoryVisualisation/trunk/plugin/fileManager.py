#!/usr/bin/python

import os.path
import messageWindow

class FileManager:
    def __init__(self, interface):
        self.__aInterface = interface
        self.__aLines = []
        self.__aCon = []
        self.__aFile = None

    def importGraph(self, paFile):
        try:
            self.__aFile = open(paFile, "r")
            try:
                sab = [a for a in self.__aInterface.templates if a.name == 'Empty Graph Theory Diagram'][0]
                sab.create_new_project()
                self.__aDiagram = list(self.__aInterface.project.root.diagrams)[0]
                self.__aLines = self.__aFile.readlines()
                elementTypeVertex = self.__aInterface.project.metamodel.elements['Vertex']
                nodes = []
                nodesValues = []

                while self.__aLines:
                    values = self.__aLines[0].split()
                    del self.__aLines[0]

                    try:
                        reverseString = values[1] + " " + values[0] + " " + values[2] + " " + "\n"
                    except IndexError:
                        reverseString = values[1] + " " + values[0] + " " + "\n"

                    elementTypeConnection = None

                    for line in self.__aLines:
                        if reverseString == line:
                            self.__aLines.remove(line)
                            elementTypeConnection = self.__aInterface.project.metamodel.connections["Edge"]

                    if not elementTypeConnection:
                        elementTypeConnection = self.__aInterface.project.metamodel.connections["Arc"]

                    if not values[0] in nodesValues:
                        self.__aDiagram.create_element(elementTypeVertex)
                        nodes.append(list(self.__aInterface.current_diagram.elements)[-1])
                        nodes[-1].object.values['name'] = values[0]
                        nodesValues.append(values[0])

                    if not values[1] in nodesValues:
                        self.__aDiagram.create_element(elementTypeVertex)
                        nodes.append(list(self.__aInterface.current_diagram.elements)[-1])
                        nodes[-1].object.values['name'] = values[1]
                        nodesValues.append(values[1])
                    
                    for node in nodes:
                        if node.object.values['name'] == values[0]:
                            nodeSource = node
                        elif node.object.values['name'] == values[1]:
                            nodeDestination = node
                    try:
                        nodeSource.connect_with(nodeDestination, elementTypeConnection)
                        con = list(nodeSource.connections)[-1]
                        con.object.values['value'] = values[2]
                    except (AttributeError,IndexError):
                        pass
            finally:
                self.__aFile.close()
        except IOError:
            pass

    def exportGraph(self, paFile):
        try:
            if self.__aInterface.project.metamodel.uri == "urn:umlfri.org:metamodel:graphTheoryVisualisation" and\
               len(list(self.__aInterface.current_diagram.connections)) > 0:
                self.__aFile = open(paFile, "w")
                self.__aLines = []
                for con in self.__aInterface.current_diagram.connections:
                    line = con.object.source.name + " " + con.object.destination.name + " " + con.object.values['value'] + "\n"
                    self.__aLines.append(line)
                    if (con.object.type.name == "Edge"):
                        line = con.object.destination.name + " " + con.object.source.name + " " + con.object.values['value'] + "\n"
                        self.__aLines.append(line)
                try:
                    self.__aFile.writelines(self.__aLines)
                finally:
                    self.__aFile.close()
            else:
                messageWindow.MessageWindow("Export Error", "Graph can be only exported from Graph Theory Diagram with\n at least 1 connection.")
        except (IOError, AttributeError):
            pass