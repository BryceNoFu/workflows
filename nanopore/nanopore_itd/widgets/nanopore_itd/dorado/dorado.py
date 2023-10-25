import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWdorado(OWBwBWidget):
    name = "dorado"
    description = "Dorado Basecaller"
    priority = 3
    icon = getIconName(__file__,"guppy1.png")
    want_main_area = False
    docker_image_name = "dorado"
    docker_image_tag = "0.3.4-linux-x64"
    inputs = [("InputDir",str,"handleInputsInputDir"),("trigger",str,"handleInputstrigger"),("trigger2",str,"handleInputstrigger2"),("reference",str,"handleInputsreference"),("OutputDir",str,"handleInputsOutputDir"),("modelFile",str,"handleInputsmodelFile")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    InputDir=pset(None)
    OutputDir=pset(None)
    modelFile=pset("dna_r9.4.1_e8_fast@v3.4")
    reference=pset(None)
    device=pset("cuda:all")
    nameSort=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"dorado")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsInputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger2(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger2", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsOutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("OutputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmodelFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("modelFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
