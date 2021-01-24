docker build -t mcvine/awsbatch_fetch_and_run .
docker tag mcvine/awsbatch_fetch_and_run:latest public.ecr.aws/y9i1c6r0/mcvine/awsbatch_fetch_and_run:latest
docker push public.ecr.aws/y9i1c6r0/mcvine/awsbatch_fetch_and_run:latest
