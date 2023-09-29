#!/bin/bash

shopt -s extglob
inputArgs=("$@")
dorado basecaller dorado-0.3.4-linux-x64/data/$modelFile $inputDir ${inputArgs[@]} | samtools sort > $outputDir/calls-sorted.bam
echo "Indexing sorted bam"
samtools index $outputDir/calls-sorted.bam

if [ -n $nameSort ]; then
	echo "Generating name sorted bam"
	samtools sort -n $outputDir/calls-sorted.bam > $outputDir/calls-name.bam
fi
