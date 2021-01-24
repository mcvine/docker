FROM mcvine/mcvine:1.4.1.dev

RUN apt-get install -y unzip zip
RUN rm -rf /var/lib/apt/lists/*
SHELL ["conda", "run", "-n", "mcvine", "/bin/bash", "-c"]
RUN which python
RUN mcvine
RUN conda install awscli

ADD fetch_and_run.sh /usr/local/bin/fetch_and_run.sh
RUN chmod +x /usr/local/bin/fetch_and_run.sh
WORKDIR /tmp
ENTRYPOINT ["/usr/local/bin/fetch_and_run.sh"]
