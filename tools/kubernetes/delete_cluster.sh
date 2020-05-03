CLUSTER_NAME="ambservice"

COMPUTE_ZONE="asia-northeast1-a"
COMPUTE_REGION="asia-northeast1"

echo "COMPUTE_ZONE="${COMPUTE_ZONE}
echo "COMPUTE_REGION="${COMPUTE_REGION}

#gcloud config set compute/zone   ${COMPUTE_ZONE}
#gcloud config set compute/region ${COMPUTE_REGION}

gcloud container clusters delete ${CLUSTER_NAME} --zone ${COMPUTE_ZONE}  
 