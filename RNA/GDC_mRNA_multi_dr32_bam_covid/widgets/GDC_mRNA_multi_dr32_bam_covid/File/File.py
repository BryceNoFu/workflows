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

class OWFile(OWBwBWidget):
    name = "File"
    description = "HISAT2 FASTQ Alignment"
    priority = 10
    icon = getIconName(__file__,"ogp.png")
    want_main_area = False
    docker_image_name = "biodepot/alpine-bash"
    docker_image_tag = "3.7"
    inputs = [("Trigger",str,"handleInputsTrigger"),("mate_1",str,"handleInputsmate_1"),("mate_2",str,"handleInputsmate_2"),("sam_output",str,"handleInputssam_output"),("hisat2_idx",str,"handleInputshisat2_idx")]
    outputs = [("File",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    hisat2_idx=pset(None)
    mate_1=pset([])
    mate_2=pset([])
    sam_output=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"File")) as f:
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
    def handleInputsmate_1(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("mate_1", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmate_2(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("mate_2", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssam_output(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sam_output", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputshisat2_idx(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("hisat2_idx", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"File"):
            outputValue=getattr(self,"File")
        self.send("File", outputValue)
