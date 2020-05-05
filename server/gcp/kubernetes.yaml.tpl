# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ambcluster-deployment
  labels:
    app: ambient_server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ambserver
  template:
    metadata:
      labels:
        app: ambserver
    spec:
      containers:
      - name: ambserver
        image: asia.gcr.io/GOOGLE_CLOUD_PROJECT/ambserver:COMMIT_SHA
        env:
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: /usr/src/app/ambmonitordev-91298aa9a897.json
        ports:
        - containerPort: 8080
---
kind: Service
apiVersion: v1
metadata:
  name: ambmonitordev
spec:
  selector:
    app: ambmonitordev
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer

