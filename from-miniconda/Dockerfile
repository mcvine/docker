FROM continuumio/miniconda

MAINTAINER "Jiao Lin <jiao.lin@gmail.com>"

LABEL Description="MCViNE software"

RUN conda config --add channels conda-forge
RUN conda config --add channels mcvine
RUN conda install numpy
RUN conda install mcvine
RUN conda install mcvine-resources
RUN conda install mcvine.phonon
RUN conda install mcvine.workflow
RUN apt-get install -y make time
