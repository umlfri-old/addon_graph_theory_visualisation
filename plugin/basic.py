
class basic:

    def __init__(self, interface, buttonMenu, initialNode):
        self.aInitialNode = initialNode
        self.aCurrentNode = self.aInitialNode
        self.aInterface = interface
        self.aButtonMenu = buttonMenu
        self.aInf = float("inf")
        self.aStep1 = False
        self.aNodes = list(self.aInterface.current_diagram.elements)
        self.aConnections = list(self.aInterface.current_diagram.connections)
        self.aStep1 = False
        self.aStep2 = False
        self.aStep3  = True

    def play(self):
        self.aButtonMenu[0].enabled = False
        self.aButtonMenu[2].enabled = False

        if not self.aStep1:
            self.step1()

        while self.aCurrentNode != self.aEndNode:
            if not self.aStep2:
                self.step2()
            elif not self.aStep3:
                self.step3()

        self.aButtonMenu[0].enabled = True
        self.aButtonMenu[2].enabled = True