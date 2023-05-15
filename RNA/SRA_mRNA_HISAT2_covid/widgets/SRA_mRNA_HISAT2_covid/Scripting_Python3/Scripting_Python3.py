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

class OWScripting_Python3(OWBwBWidget):
    name = "Scripting_Python3"
    description = "Minimum Python3 container with pip"
    priority = 10
    icon = getIconName(__file__,"python3.png")
    want_main_area = False
    docker_image_name = "biodepot/python"
    docker_image_tag = "3.10.9__alpine-3.17.1__8132a508__2132c733__29cfe2a0"
    inputs = [("InputFile",str,"handleInputsInputFile"),("Trigger",str,"handleInputsTrigger"),("work_dir",str,"handleInputswork_dir"),("sra_ids",str,"handleInputssra_ids")]
    outputs = [("OutputDir",str),("fastq_mate1",str),("fastq_mate2",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    InputFile=pset(None)
    work_dir=pset(None)
    sra_ids=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Scripting_Python3")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsInputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputswork_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("work_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssra_ids(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sra_ids", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
        outputValue=None
        if hasattr(self,"fastq_mate1"):
            outputValue=getattr(self,"fastq_mate1")
        self.send("fastq_mate1", outputValue)
        outputValue=None
        if hasattr(self,"fastq_mate2"):
            outputValue=getattr(self,"fastq_mate2")
        self.send("fastq_mate2", outputValue)
