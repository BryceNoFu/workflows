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

class OWStart(OWBwBWidget):
    name = "Start"
    description = "Enter workflow parameters and start"
    priority = 10
    icon = getIconName(__file__,"start.png")
    want_main_area = False
    docker_image_name = "biodepot/hisat2-mrna-start"
    docker_image_tag = "latest"
    outputs = [("work_dir",str),("genome_dir",str),("genome_file",str),("sra_ids",str),("mate_1",str),("mate_2",str),("unpaired",str),("sam_output",str),("hisat2_idx",str),("annotation_gtf",str),("gzip",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    work_dir=pset(None)
    genome_file=pset(None)
    sra_ids=pset([])
    genome_dir=pset(None)
    basename=pset("genome")
    annotation_gtf=pset(None)
    mate_1=pset([])
    mate_2=pset([])
    unpaired=pset([])
    sam_output=pset([])
    hisat2_idx=pset(None)
    gzip=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Start")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"work_dir"):
            outputValue=getattr(self,"work_dir")
        self.send("work_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_dir"):
            outputValue=getattr(self,"genome_dir")
        self.send("genome_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_file"):
            outputValue=getattr(self,"genome_file")
        self.send("genome_file", outputValue)
        outputValue=None
        if hasattr(self,"sra_ids"):
            outputValue=getattr(self,"sra_ids")
        self.send("sra_ids", outputValue)
        outputValue=None
        if hasattr(self,"mate_1"):
            outputValue=getattr(self,"mate_1")
        self.send("mate_1", outputValue)
        outputValue=None
        if hasattr(self,"mate_2"):
            outputValue=getattr(self,"mate_2")
        self.send("mate_2", outputValue)
        outputValue=None
        if hasattr(self,"unpaired"):
            outputValue=getattr(self,"unpaired")
        self.send("unpaired", outputValue)
        outputValue=None
        if hasattr(self,"sam_output"):
            outputValue=getattr(self,"sam_output")
        self.send("sam_output", outputValue)
        outputValue=None
        if hasattr(self,"hisat2_idx"):
            outputValue=getattr(self,"hisat2_idx")
        self.send("hisat2_idx", outputValue)
        outputValue=None
        if hasattr(self,"annotation_gtf"):
            outputValue=getattr(self,"annotation_gtf")
        self.send("annotation_gtf", outputValue)
        outputValue=None
        if hasattr(self,"gzip"):
            outputValue=getattr(self,"gzip")
        self.send("gzip", outputValue)
