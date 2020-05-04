#
# Set key ring name and key name. 
#
_keyring_name=$GCP_KMS_KEYRING
_key_name=$GCP_KMS_KEY

#
# Initial time to create keyring and key
#
#gcloud kms keyrings create ${_keyring_name} --location=global
#gcloud kms keys create ${_key_name} --location=global --keyring=${_keyring_name} --purpose=encryption
#
# list key name
#
echo "gcloud kms keys list --location global --keyring "$_keyring_name
gcloud kms keys list --location global --keyring $_keyring_name