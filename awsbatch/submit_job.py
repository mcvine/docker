#!/usr/bin/env python
"""
Each job has a unique directory in {s3projectdir}/jobs/
It contains

* The data zip file
"""

s3bucket = 'sts-mcvine'
s3projectdir = "batch"
s3jobsdir = s3projectdir + "/jobs"
# s3jobsdir: batch/jobs
# its full url: s3://sts-mcvine/batch/jobs/

import os, sh, boto3
aws_settings = dict(
    AWS_DEFAULT_REGION = "us-east-1",
    # AWS_ACCESS_KEY_ID = "XXX",
    # AWS_SECRET_ACCESS_KEY = "xxx"
)
# os.environ.update(aws_settings)

def submit(
        name, zippath, cmd,
        definition="mcvine_fetch_and_run_16cores_32G_3hours:1",
        wait=False,
        queue="mcvine-16-queue"):
    """
    """
    if zippath.startswith('s3://'):
        assert zippath.startswith('s3://'+s3bucket)
    uniquename = unique_name(name)
    s3jobdir = '{}/{}'.format(s3jobsdir, uniquename)
    s3zippath = prepare_s3_jobdir(zippath, cmd, s3jobdir)
    import time
    client = boto3.client('batch')
    env = []
    zipbasename = os.path.basename(zippath)
    command = [
        s3bucket, s3zippath.lstrip('s3://'+s3bucket), cmd,
        '{}/out.zip'.format(s3jobdir)]
    print(command)
    response = client.submit_job(
        jobName=uniquename,
        jobQueue='arn:aws:batch:us-east-1:668650830132:job-queue/{}'.format(queue),
        jobDefinition=('arn:aws:batch:us-east-1:668650830132:'
                       'job-definition/{}'.format(definition)),
        containerOverrides=dict(environment=env, command=command),
    )
    print(response)
    if not wait: return
    finished = False
    while not finished:
        time.sleep(60)
        resps = client.describe_jobs(jobs=[response['jobId']])
        for resp in resps['jobs']:
            status = resp['status']
            print(resp['jobName'], status)
            finished = status in ['SUCCEEDED', 'FAILED']
            if finished: break
    return

def prepare_s3_jobdir(zippath, cmd, s3jobdir):
    s3cp = sh.aws.bake('s3', 'cp')
    join = os.path.join
    s3jobdirurl = 's3://{}/{}'.format(s3bucket, s3jobdir)
    if not zippath.startswith('s3://'):
        zipbasename = os.path.basename(zippath)
        s3zippath = join(s3jobdirurl, zipbasename)
        print(zippath, s3zippath)
        s3cp(zippath, s3zippath)
    else:
        s3zippath = zippath
    # create file to save script to run
    import tempfile
    tmpdir = tempfile.mkdtemp()
    run_sh = os.path.join(tmpdir, 'run.sh')
    with open(run_sh, 'wt') as stream:
        stream.write(cmd)
    print(run_sh, join(s3jobdirurl, 'run.sh'))
    s3cp(run_sh, join(s3jobdirurl, 'run.sh'))
    return s3zippath

def unique_name(name):
    from datetime import datetime
    # datetime object containing current date and time
    now = datetime.now()
    now = now.strftime("%Y%m%d_%H%M%S")
    import uuid; uuid = uuid.uuid4().hex[:6].upper()
    return "{}-{}-{}".format(now, uuid, name)

def sendemail(from_address, to_addresses, subject, body):
    client = boto3.client(
        'ses',
        region_name=aws_settings['AWS_DEFAULT_REGION'],
        aws_access_key_id=aws_settings['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=aws_settings['AWS_SECRET_ACCESS_KEY']
    )
    response = client.send_email(
        Destination={
            'ToAddresses': to_addresses,
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=from_address,
    )
    return
