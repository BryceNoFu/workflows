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

class OWJupyter_jupyter_sleuth_1_2(OWBwBWidget):
    name = "Jupyter_jupyter_sleuth_1_2"
    description = "Base installation of Jupyter"
    priority = 103
    icon = getIconName(__file__,"jupyter-sleuth.png")
    want_main_area = False
    docker_image_name = "biodepot/jupyter-sleuth"
    docker_image_tag = "0.30.1__bioc-r_3.16-ubuntu-22.04-r-4.2.2__4c9bf054__69053778__f653260c"
    inputs = [("InputDir",str,"handleInputsInputDir"),("Trigger",str,"handleInputsTrigger"),("startingNotebook",str,"handleInputsstartingNotebook")]
    outputs = [("OutputDir",str),("outputNotebook",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    subcommand=pset("notebook")
    execute=pset(False)
    startingNotebook=pset(None)
    type=pset("notebook")
    outputNotebook=pset(None)
    debug=pset(False)
    generateConfig=pset(False)
    autoyes=pset(True)
    allowRoot=pset(True)
    loglevel=pset("30")
    ip=pset("0.0.0.0")
    port=pset(8888)
    config=pset(None)
    transport=pset(None)
    keyfile=pset(None)
    certfile=pset(None)
    clientca=pset(None)
    nomathjax=pset(False)
    browser=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Jupyter_jupyter_sleuth_1_2")) as f:
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
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsstartingNotebook(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("startingNotebook", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
        outputValue=None
        if hasattr(self,"outputNotebook"):
            outputValue=getattr(self,"outputNotebook")
        self.send("outputNotebook", outputValue)
