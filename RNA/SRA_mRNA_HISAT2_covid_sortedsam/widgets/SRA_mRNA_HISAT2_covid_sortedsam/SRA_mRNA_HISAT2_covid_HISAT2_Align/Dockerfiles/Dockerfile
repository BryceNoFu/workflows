FROM ubuntu:22.04

# Copy hisat2 shell script and make executable
COPY runHisat.sh ./runHisat.sh
RUN chmod +x runHisat.sh

# Install hisat2
RUN apt update && apt -y install hisat2=2.2.1-3