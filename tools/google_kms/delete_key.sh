#
# https://cloud.google.com/kms/docs/rotating-keys?hl=ja
#
echo "Please check the version of the key."
echo "gcloud kms keys versions list --location global --keyring "$_keyring_name" --key "$_key_name
gcloud kms keys versions list --location global --keyring $_keyring_name --key $_key_name

#
# 
#
_key_version="1"
echo "Please run the delete command"
echo "gcloud kms keys versions destroy "$_key_version" --location global --keyring "$_keyring_name" --key "$_key_name
#gcloud kms keys versions destroy $_key_version --location global --keyring $_keyring_name --key $_key_name
