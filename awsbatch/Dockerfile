FROM mcvine/mcvine:1.4.1.dev

RUN rm -rf /var/lib/apt/lists/*
ADD fetch_and_run.sh /usr/local/bin/fetch_and_run.sh

RUN which python
RUN conda install awscli

USER nobody
WORKDIR /tmp
ENTRYPOINT ["/usr/local/bin/fetch_and_run.sh"]
