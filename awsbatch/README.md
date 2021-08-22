TODO: 
* Limit permissions
* change s3 bucket
* change compute env to have ssh key. change security group
* use m4.16x for compute env?

# Compute env
## mcvine-16VCPU-100G_STORAGE
* Managed
* Service role: AWSBatchServiceRole
* Instancerole: ecsInstanceRole
* On-demand
* Min vCPUs: 0
* Max vCPUs: 16
* Desired vCPUs: 16
* Allowed instance types: optimized
* Allocation strategy: BEST_FIT
* Launch-template: increase-volume (see the script and json file)
* Networking: vpc

# Job definition
## mcvine_fetch_and_run_16cores_32G_3hours_100G
* Platform: EC2
* Container
  - Image: public.ecr.aws/y9i1c6r0/mcvine/awsbatch_fetch_and_run
  - vCPUs: 16
  - Memory: 32768
  - Job role: batchJobRole
  - Execution role: batchJobRole
  - Volumes
    - Name: host_tmp
    - Source path: /tmp
  - Mount points
    - Source volume: host_tmp
    - Container path: /work
  - Env vars
    - OMPI_ALLOW_RUN_AS_ROOT: 1
    - OMPI_ALLOW_RUN_AS_ROOT_CONFIRM: 1
  - Security
    - User: root

