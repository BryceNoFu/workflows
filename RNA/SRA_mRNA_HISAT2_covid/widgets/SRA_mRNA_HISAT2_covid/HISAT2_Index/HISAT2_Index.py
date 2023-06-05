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
    docker_image_name = "brycenofu/hisat2"
    docker_image_tag = "ubuntu22.04"
    inputs = [("Trigger",str,"handleInputsTrigger"),("reference_in",str,"handleInputsreference_in"),("ht2_idx",str,"handleInputsht2_idx")]
    outputs = [("ht2_base",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    reference_in=pset(None)
    ht2_idx=pset(None)
    p=pset(1)
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
    def handleInputsht2_idx(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("ht2_idx", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"ht2_base"):
            outputValue=getattr(self,"ht2_base")
        self.send("ht2_base", outputValue)
