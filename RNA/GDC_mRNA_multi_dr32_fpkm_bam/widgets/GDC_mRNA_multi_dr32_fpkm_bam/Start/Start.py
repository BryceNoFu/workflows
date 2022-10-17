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
    docker_image_name = "biodepot/gdc-mrna-start"
    docker_image_tag = "alpine_3.12.1__384d16ee"
    outputs = [("work_dir",str),("genome_dir",str),("genome_file",str),("annotation_file",str),("geneinfo",str),("bypass_star_index",str),("gdc_credentials",str),("gdc_token",str),("bam_uuid",str),("bam_file",str),("fastq1_files",str),("fastq2_files",str),("fastqo1_files",str),("fastqo2_files",str),("fastqs_files",str),("biobambam_files",str),("bypass_biobambam",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    work_dir=pset(None)
    genome_dir=pset(None)
    genome_file=pset(None)
    annotation_file=pset(None)
    geneinfo=pset(None)
    bypass_star_index=pset(True)
    gdc_credentials=pset(None)
    gdc_token=pset(None)
    bam_uuid=pset(None)
    bam_file=pset([])
    fastq1_files=pset([])
    fastq2_files=pset([])
    fastqo1_files=pset([])
    fastqo2_files=pset([])
    fastqs_files=pset([])
    paired_end=pset(True)
    biobambam_files=pset([])
    prepend_date=pset(False)
    bypass_biobambam=pset(False)
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
        if hasattr(self,"annotation_file"):
            outputValue=getattr(self,"annotation_file")
        self.send("annotation_file", outputValue)
        outputValue=None
        if hasattr(self,"geneinfo"):
            outputValue=getattr(self,"geneinfo")
        self.send("geneinfo", outputValue)
        outputValue=None
        if hasattr(self,"bypass_star_index"):
            outputValue=getattr(self,"bypass_star_index")
        self.send("bypass_star_index", outputValue)
        outputValue=None
        if hasattr(self,"gdc_credentials"):
            outputValue=getattr(self,"gdc_credentials")
        self.send("gdc_credentials", outputValue)
        outputValue=None
        if hasattr(self,"gdc_token"):
            outputValue=getattr(self,"gdc_token")
        self.send("gdc_token", outputValue)
        outputValue=None
        if hasattr(self,"bam_uuid"):
            outputValue=getattr(self,"bam_uuid")
        self.send("bam_uuid", outputValue)
        outputValue=None
        if hasattr(self,"bam_file"):
            outputValue=getattr(self,"bam_file")
        self.send("bam_file", outputValue)
        outputValue=None
        if hasattr(self,"fastq1_files"):
            outputValue=getattr(self,"fastq1_files")
        self.send("fastq1_files", outputValue)
        outputValue=None
        if hasattr(self,"fastq2_files"):
            outputValue=getattr(self,"fastq2_files")
        self.send("fastq2_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqo1_files"):
            outputValue=getattr(self,"fastqo1_files")
        self.send("fastqo1_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqo2_files"):
            outputValue=getattr(self,"fastqo2_files")
        self.send("fastqo2_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqs_files"):
            outputValue=getattr(self,"fastqs_files")
        self.send("fastqs_files", outputValue)
        outputValue=None
        if hasattr(self,"biobambam_files"):
            outputValue=getattr(self,"biobambam_files")
        self.send("biobambam_files", outputValue)
        outputValue=None
        if hasattr(self,"bypass_biobambam"):
            outputValue=getattr(self,"bypass_biobambam")
        self.send("bypass_biobambam", outputValue)
