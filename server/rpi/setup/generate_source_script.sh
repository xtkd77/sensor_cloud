#!/bin/bash

project=$(gcloud config get-value core/project 2> /dev/null)
echo ""
echo "Current Google Cloud Platform project is "$project
echo ""

GIT_ROOTDIR=`git rev-parse --show-superproject-working-tree --show-toplevel`
echo "ROOTDIR is "$GIT_ROOTDIR

cat <<EOF > source_file.txt

export PROJECT=$project
export GOOGLE_APPLICATION_CREDENTIALS=${GIT_ROOTDIR}/server/rpi/ambmonitordev-91298aa9a897.json

EOF


echo "======================================================"
echo ""
echo "Please run: "
echo "$ source source_file.txt"
echo ""
echo "======================================================"
