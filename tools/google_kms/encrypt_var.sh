#!/bin/bash

_keyring_name=$GCP_KMS_KEYRING
_key_name=$GCP_KMS_KEY
echo "keyring="$_keyring_name
echo "key="$_key_name

echo -n $MY_SECRET | gcloud kms encrypt \
    --plaintext-file=- \
    --ciphertext-file=- \
    --location=global \
    --keyring=$_keyring_name \
    --key=$_key_name | base64 | tr -d '\n'

echo ""
echo "-------------------------"


