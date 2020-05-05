#!/bin/bash

#
# Set key ring name and key name. 
#
_keyring_name=$GCP_KMS_KEYRING
_key_name=$GCP_KMS_KEY

#
# list key name
#
echo "gcloud kms keys list --location global --keyring "$_keyring_name
gcloud kms keys list --location global --keyring $_keyring_name

ENC_FILE=$1
PLAIN_FILE=$ENC_FILE.".plain"
#gcloud kms encrypt --plaintext-file=${PLAIN_FILE} --ciphertext-file=${ENC_FILE} --location=global --keyring=${_keyring_name} --key=${_key_name}


gcloud kms decrypt \
       --ciphertext-file=${ENC_FILE} \
       --plaintext-file=${PLAIN_FILE} \
       --location=global --keyring=${_keyring_name}  --key=${_key_name}


