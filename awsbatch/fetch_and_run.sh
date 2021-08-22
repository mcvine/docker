#!/bin/bash
# fetch_and_run.sh "s3bucket" "data.zip" "cmd" "out.zip"
# fetch_and_run.sh "sts-mcvine" "job1/data.zip" "python scripts/sim.py --angle 1." "job1/out.zip"

# PATH="/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
# get args
S3_BUCKET=$1
ZIPFILE=$2
CMD=$3
OUT=$4
ZIP_URL="s3://"$S3_BUCKET/$ZIPFILE
OUTZIP_URL="s3://"$S3_BUCKET/$OUT
WORKDIR=$PWD

# conda
eval "$(conda shell.bash hook)"
conda activate mcvine

BASENAME="${0##*/}"

# Standard function to print an error and exit with a failing return code
error_exit () {
    echo "${BASENAME} - ${1}" >&2
    exit 1
}

# Check that necessary programs are available
which aws >/dev/null 2>&1 || error_exit "Unable to find AWS CLI executable."
which unzip >/dev/null 2>&1 || error_exit "Unable to find unzip executable."
which zip >/dev/null 2>&1 || error_exit "Unable to find zip executable."

# Create a temporary directory to hold the downloaded contents, and make sure
# it's removed later, unless the user set KEEP_BATCH_FILE_CONTENTS.
cleanup () {
    if [ -z "${KEEP_BATCH_FILE_CONTENTS}" ] \
           && [ -n "${TMPDIR}" ] \
           && [ "${TMPDIR}" != "/" ]; then
        rm -r "${TMPDIR}"
    fi
}
trap 'cleanup' EXIT HUP INT QUIT TERM
# mktemp arguments are not very portable.  We make a temporary directory with
# portable arguments, then use a consistent filename within.
TMPDIR="$(mktemp -d -p ${WORKDIR} -t tmp.XXXXXXXXX)" || error_exit "Failed to create temp directory."
TMPFILE="${TMPDIR}/batch-file-temp"
install -m 0600 /dev/null "${TMPFILE}" || error_exit "Failed to create temp file."

# fetch zip file
# Download a zip 
fetch_and_run_zip () {
    # Create a temporary file and download the zip file
    aws s3 cp "${ZIP_URL}" - > "${TMPFILE}" || error_exit "Failed to download S3 zip file from ${ZIP_URL}"

    # Create a temporary directory and unpack the zip file
    cd "${TMPDIR}" || error_exit "Unable to cd to temporary directory."
    echo "${TMPDIR}"
    unzip -q "${TMPFILE}" || error_exit "Failed to unpack zip file."

    bash -c "${CMD}" || error_exit "Failed to execute ${CMD}"

    zip -r out.zip out/ || error_exit "Failed to zip output directory"
    aws s3 cp out.zip ${OUTZIP_URL} || error_exit "Failed to copy output zip to $OUTZIP_URL"
}

fetch_and_run_zip
