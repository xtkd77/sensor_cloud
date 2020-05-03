#!/bin/bash
#
#
#
# https://cloud.google.com/compute/docs/regions-zones
# リージョン asia-northeast1
# ゾーン asia-northeast1-a
#　ロケーション 東京（日本）
#

CLUSTER_NAME="ambcluster"

COMPUTE_ZONE="asia-northeast1-a"
COMPUTE_REGION="asia-northeast1"

echo "COMPUTE_ZONE="${COMPUTE_ZONE}
echo "COMPUTE_REGION="${COMPUTE_REGION}

gcloud config set compute/zone   ${COMPUTE_ZONE}
gcloud config set compute/region ${COMPUTE_REGION}

#gcloud container clusters create ${CLUSTER_NAME} \
#    --zone ${COMPUTE_ZONE}  \
#    --num-nodes=1 --max-nodes=2

# Kubernetes Engin のトラブルシューティング
# https://cloud.google.com/kubernetes-engine/docs/troubleshooting?hl=ja
#
gcloud container clusters create ${CLUSTER_NAME}\
    --zone ${COMPUTE_ZONE} \
    --no-enable-basic-auth\
    --cluster-version "1.14.10-gke.27" --machine-type "n1-standard-1"\
    --image-type "COS" --disk-type "pd-standard" --disk-size "100"\
    --metadata disable-legacy-endpoints=true\
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "3" --enable-stackdriver-kubernetes --enable-ip-alias --network "projects/ambmonitordev/global/networks/default" --subnetwork "projects/ambmonitordev/regions/asia-northeast1/subnetworks/default"\
    --default-max-pods-per-node "10"\
    --no-enable-master-authorized-networks\
    --addons HorizontalPodAutoscaling,HttpLoadBalancing\
    --enable-autoupgrade --enable-autorepair
