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

class OWNextflow(OWBwBWidget):
    name = "Nextflow"
    description = "Run a nextflow file"
    priority = 10
    icon = getIconName(__file__,"wGgCniy6_400x400.png")
    want_main_area = False
    docker_image_name = "nextflow/nextflow"
    docker_image_tag = "22.10.8"
    inputs = [("inputFile",str,"handleInputsinputFile"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    InputFile=pset(None)
    input=pset(None)
    outdir=pset(None)
    genome=pset(None)
    profile=pset("docker")
    gtf_file=pset(None)
    gff_file=pset(None)
    transcript_fasta=pset(None)
    additional_fasta=pset(None)
    bbsplit_fasta_list=pset(None)
    salmon_index=pset(None)
    hisat2_index=pset(None)
    rsem_index=pset(None)
    aligner=pset(None)
    pseudo_aligner=pset(None)
    skip_bbsplit=pset(False)
    umitools_bc_pattern=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Nextflow")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
