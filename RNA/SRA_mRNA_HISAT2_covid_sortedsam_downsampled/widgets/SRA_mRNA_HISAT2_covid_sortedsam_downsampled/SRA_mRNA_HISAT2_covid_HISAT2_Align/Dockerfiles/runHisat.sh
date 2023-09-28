#!/bin/bash

#pass the file lists in the widgets as environment variables mate1, mate2, and unpaired

listToCsv () {
   #the list comes in the form ["file1","file2", ...]
   #this version removes the [] and removes the quotes if any to convert it to a csv string
   echo $1 | sed 's/"//g' | sed 's/\[//g' | sed 's/\]//g'
}

#if there is a value to $mate1, then we have paired end reads
if [ -n "$mate1" ]; then
   filestring="-1 $(listToCsv $mate1) -2 $(listToCsv $mate2) "
elif [ -n "$unpaired" ]; then
   filestring="-U (listToCsv $unpaired) "
elif [ -n "$sraids" ]; then
   filestring="--sra-acc $(listToCsv $sraids) "
else
   echo "No input files found"
   exit 1
fi

#The command line is $@ so we put the filestring at the end and execute it using the eval command
echo "hisat2 $@ $filestring "
eval "hisat2 $@ $filestring "