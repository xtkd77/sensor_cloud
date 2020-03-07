"""
Google Storage にデータをPublish/Subscribe するためのインターフェイスを実装します。

[参考]
https://google-cloud-python.readthedocs.io/en/0.32.0/pubsub/index.html
https://googleapis.dev/python/pubsub/latest/index.html

[python 準備 (linux)]
python3 -m pip install virtualenv
virtualenv myenv
source ./myenv/bin/activate
./myenv/bin/pip install -r requirements.txt

[python 準備 (powershell)]
python3 -m pip install virtualenv
virtualenv myenv
Set-ExecutionPolicy RemoteSigned -Scope Process # -forceオプションで省略可
.\myenv\Scripts\activate

[Google Cloud Platform の認証関係の用意]
gcloud auth login
gcloud config set project <project_id>
export GOOGLE_APPLICATION_CREDENTIALS <credential file>


[準備の準備]
pipreqs .
"""

from google.cloud import pubsub_v1
import os

project_id = ""
topic_name = ""


def initialize():
    global project_id
    global topic_name
    project_id = os.environ["PROJECT_ID"]
    topic_name = os.environ["GCP_DEFAULT_TOPIC_NAME"]

def register_device(device_info):
    """ Create topic for the new device. """

    publisher = pubsub.PublisherClient()
    topic = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic='MY_TOPIC_NAME',  # Set this to something appropriate.
    )
    publisher.create_topic(topic)  # raises conflict if topic exists
    publisher.publish(topic, b'My first message!', spam='eggs')


def publish_msg(device_name, data):
    """ Publish the message of given data.
    
    Returns
    -------
    message_id:int, Google PubSub message ID
    """

    publisher = pubsub_v1.PublisherClient() # .from_service_account_file(credential_file)
    future = publisher.publish(publisher.topic_path(project_id, topic_name), data)
    message_id = future.result(timeout=10)
    return message_id

# end of gcp_pubsub.py