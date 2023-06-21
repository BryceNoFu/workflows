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

class OWHISAT2_Index(OWBwBWidget):
    name = "HISAT2_Index"
    description = "hisat2 index builder"
    priority = 10
    icon = getIconName(__file__,"ogp.png")
    want_main_area = False
    docker_image_name = "biodepot/hisat2"
    docker_image_tag = "latest"
    inputs = [("Trigger",str,"handleInputsTrigger"),("reference_in",str,"handleInputsreference_in"),("hisat2_idx",str,"handleInputshisat2_idx")]
    outputs = [("hisat2_idx",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    reference_in=pset(None)
    hisat2_idx=pset(None)
    nthreads=pset(1)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"HISAT2_Index")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference_in(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference_in", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputshisat2_idx(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("hisat2_idx", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"hisat2_idx"):
            outputValue=getattr(self,"hisat2_idx")
        self.send("hisat2_idx", outputValue)
