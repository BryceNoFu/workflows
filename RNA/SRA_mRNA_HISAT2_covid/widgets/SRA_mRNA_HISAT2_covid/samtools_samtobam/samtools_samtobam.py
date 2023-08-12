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

class OWsamtools_samtobam(OWBwBWidget):
    name = "samtools_samtobam"
    description = "SamTools SAM file to BAM file"
    priority = 10
    icon = getIconName(__file__,"samsort.png")
    want_main_area = False
    docker_image_name = "brycenofu/samtools-samtobam"
    docker_image_tag = "latest"
    inputs = [("samFile",str,"handleInputssamFile")]
    outputs = [("fin",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    samFile=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"samtools_samtobam")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputssamFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("samFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"fin"):
            outputValue=getattr(self,"fin")
        self.send("fin", outputValue)
