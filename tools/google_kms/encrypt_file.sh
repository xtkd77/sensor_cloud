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

PLAIN_FILE=$1
ENC_FILE=$PLAIN_FILE".enc"
gcloud kms encrypt --plaintext-file=${PLAIN_FILE} --ciphertext-file=${ENC_FILE} --location=global --keyring=${_keyring_name} --key=${_key_name}
