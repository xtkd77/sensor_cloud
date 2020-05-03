#!/bin/bash

gcloud container clusters get-credentials ambcluster --zone asia-northeast1-a --project ambmonitordev
kubectl.exe get pod

