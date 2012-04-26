#!/usr/bin/python

import os.path

class FileManager:
    def __init__(self, interface):
        self.__aInterface = interface
        self.__aLines = []
        self.__aCon = []
        self.__aFile = None

    def importGraph(self):
        try:
            self.__aFile = open("c:\Loki\myGraph.txt", "r")
            try:
                self.__aLines = self.__aFile.readlines()
                elementTypeVertex = self.__aInterface.project.metamodel.elements['Vertex']
                elementTypeConnection = None
                nodes = []
                nodesValues = []

                while self.__aLines:
                    values = self.__aLines[0].split()
                    del self.__aLines[0]

                    if not elementTypeConnection:
                        elementTypeConnection = self.__aInterface.project.metamodel.connections[values[3]]

                    if not values[0] in nodesValues:
                        self.__aInterface.current_diagram.create_element(elementTypeVertex)
                        nodes.append(list(self.__aInterface.current_diagram.elements)[-1])
                        nodes[-1].object.values['name'] = values[0]
                        nodesValues.append(values[0])

                    if not values[1] in nodesValues:
                        self.__aInterface.current_diagram.create_element(elementTypeVertex)
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
                    except AttributeError:
                        pass
            finally:
                self.__aFile.close()
        except IOError:
            pass

    def exportGraph(self):
        try:
            self.__aFile = open("c:\Loki\myGraph.txt", "w")
            self.__aLines = []
            for con in self.__aInterface.current_diagram.connections:
                line = con.object.source.name + " " + con.object.destination.name + " " + con.object.values['value'] + " " + con.object.type.name + "\n"
                self.__aLines.append(line)
            try:
                self.__aFile.writelines(self.__aLines)
            finally:
                self.__aFile.close()
        except IOError:
            pass