"""
Google Cloud Storage にファイルをupload / download するための関数です。
使用する前に以下のことがしてあることを前提にしています。
(1) キーの鍵を環境変数 GOOGLE_APPLICATION_CREDENTIAL に設定する
(2) bucket は作成してある

            (C) TORUPA Laboraty 2020
"""
import google.cloud.storage as storage
from os import path, environ

def upload_file(local_fpath:str, bucket_name:str, remote_fpath:str):
    """
    ファイルをアップロードします。
    """
    #st_client = storage.Client.from_service_account_json(kwargs["credential_file"])
    client = storage.Client()
    assert isinstance(client, storage.Client)
    bucket = client.lookup_bucket(bucket_name)
    assert isinstance(bucket, storage.bucket.Bucket)
    if not path.isfile(local_fpath):
        print("({}) local file {} not found.".format(__name__, local_fpath) )
        return ""
    blob = bucket.blob(remote_fpath)
    if blob is not None:
        blob.upload_from_filename(local_fpath)
        print(__name__, ' upload {} to {}.'.format(local_fpath, remote_fpath))
        url = "https://console.cloud.google.com/storage/browser/{}/{}".format(bucket_name, remote_fpath)
        return url
    return ""


def download_file(bucket_name:str, remote_fpath:str, local_fpath:str):
    """
    kwargs
    -- crendeital_file
    """
    client = storage.Client()
    assert isinstance(client, storage.Client)
    bucket = client.lookup_bucket(bucket_name)
    assert isinstance(bucket, storage.bucket.Bucket)
    blob = bucket.blob(remote_fpath)
    if blob is not None:
        blob.download_to_filename(local_fpath)
        print(__name__, ' download {} to {}.'.format(local_fpath, remote_fpath))
    return ""


def test_bucket():
    client = storage.Client()
    for bucket in client.list_buckets():
        print(bucket)

def test_list_blob(bucket_name):
    print("test_list_blob")
    client = storage.Client()
    assert isinstance(client, storage.Client)
    bucket = client.get_bucket(bucket_name)
    assert isinstance(bucket, storage.bucket.Bucket)
    dirs = bucket.list_blobs(prefix="test/dir01")
    [ print(b) for b in dirs ]


def test_upload_file():
    print("GOOGLE_APPLICATION_CREDENTIALS={}".format(environ.get("GOOGLE_APPLICATION_CREDENTIALS")))
    test_bucket()

    local_file = path.abspath(__file__)
    bucket_name = "mqtt-log-test"
    remote_filepath = "test/dir01/"+ path.basename(local_file)
    
    upload_file(local_file, bucket_name, remote_filepath)

    download_file(bucket_name, remote_filepath, "testdonwloadfile")
    
    test_list_blob(bucket_name)

if __name__ == "__main__":
    test_upload_file()
