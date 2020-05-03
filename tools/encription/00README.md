## Ggoogle Key Management System の使い方メモ

# 暗号化の操作について 
- 参考: https://cloud.google.com/kms/docs/quickstart?hl=ja

- 操作は、console.google.cloud.com の セキュリティ / 暗号鍵　からも行える。

# Cloud build での使い方

- 参考：https://cloud.google.com/cloud-build/docs/securing-builds/use-encrypted-secrets-credentials?hl=ja

そのまま cloudbuild.yaml の step: に書けばＯＫかな、と思い、動かしてみると、みごとにエラーになります。

```
ERROR: (gcloud.kms.decrypt) PERMISSION_DENIED: Permission 'cloudkms.cryptoKeyVersions.useToDecrypt' denied on resource 'projects/my-project/locations/global/keyRings/mykeyring/cryptoKeys/mykey' (or it may not exist).
```


