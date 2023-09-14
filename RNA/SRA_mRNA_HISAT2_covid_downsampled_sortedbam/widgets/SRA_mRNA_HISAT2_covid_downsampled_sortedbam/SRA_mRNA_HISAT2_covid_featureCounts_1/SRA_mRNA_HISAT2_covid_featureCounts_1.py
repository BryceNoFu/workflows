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

class OWSRA_mRNA_HISAT2_covid_featureCounts_1(OWBwBWidget):
    name = "SRA_mRNA_HISAT2_covid_featureCounts_1"
    description = "featureCounts sam to counts"
    priority = 10
    icon = getIconName(__file__,"SubreadSmallLogo.png")
    want_main_area = False
    docker_image_name = "biodepot/subread"
    docker_image_tag = "latest"
    inputs = [("Trigger",str,"handleInputsTrigger"),("sambam_input",str,"handleInputssambam_input"),("annotation_gtf",str,"handleInputsannotation_gtf")]
    outputs = [("counts_output",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    annotation_gtf=pset(None)
    counts_output=pset(None)
    sambam_input=pset([])
    paired_end_inputs=pset(False)
    paired_end_reads=pset(False)
    nthreads=pset(None)
    gtf_annotation=pset(None)
    gtf_attribute=pset(None)
    strand_specific=pset(1)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"SRA_mRNA_HISAT2_covid_featureCounts_1")) as f:
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
    def handleInputssambam_input(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sambam_input", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsannotation_gtf(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("annotation_gtf", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"counts_output"):
            outputValue=getattr(self,"counts_output")
        self.send("counts_output", outputValue)
