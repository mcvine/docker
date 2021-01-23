FROM continuumio/miniconda3

MAINTAINER "Jiao Lin <jiao.lin@gmail.com>"

LABEL Description="MCViNE software"

RUN apt-get install -y make time

RUN conda config --add channels conda-forge
RUN conda config --add channels diffpy
RUN conda config --add channels mantid
RUN conda config --add channels mcvine
RUN conda create -n mcvine -c mcvine/label/unstable mcvine=1.4.0 mcvine-core=1.4.1.dev python=3 openmpi
SHELL ["conda", "run", "-n", "mcvine", "/bin/bash", "-c"]
RUN git clone https://github.com/yxqd/dotmantid ~/.mantid
RUN mcvine