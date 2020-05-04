#!/bin/bash
#https://cloud.google.com/storage/docs/json_api/v1/objects/list

#curl http://content-storage.googleapis.com/storage/v1/b/mqtt-log-test/o?prefix=test%2Fdir01&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM

curl 'https://storage.googleapis.com/storage/v1/b/mqtt-log-test/o?prefix=test%2Fdir01' \
    --header 'Authorization: Bearer ya29.a0Ae4lvC0sTTgS_1OahisGPAnQ56xruribVp0U9yQoTgkF9wzEcZfJDH3lWwU6s1M7qpocjBPq2l9_MMMVMueltHm-FY_6M0_iXDupf51oETkgvMdC5PbtuPUAYASv60ngmGK0F0k446SEMR8rvSpzU533bzZ3zVjT2FQ' \
    --header 'Accept: application/json' \
    --compressed

