FROM nvidia/cuda:11.1.1-base-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y wget bc rsync samtools && rm -rf /var/lib/apt/lists/
RUN wget -qO- https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.3.4-linux-x64.tar.gz | tar -xzvf -
ENV PATH="${PWD}/dorado-0.3.4-linux-x64/bin:${PATH}"
RUN mkdir -p dorado-0.3.4-linux-x64/data/ && dorado download --directory dorado-0.3.4-linux-x64/data/
COPY runDorado.sh ./runDorado.sh
RUN chmod +x runDorado.sh
