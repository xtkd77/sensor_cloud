# -*- coding: utf-8 -*-
"""
センサーロガーのメッセージを受信してファイルに保存するMQTT Client と、保存したファイルをGoogle Cloud Storage に upload する機能を実装ています。

MQTT client は下記のプログラムを参考にしました。
https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub-class.py

このプログラムを使用するときは、環境変数 
"CLOUDMQTT_KEY" にMQTT broker へのアクセスする情報
"GOOGLE_APPLICATION_CREDENTIALS" Storage にアクセス権のあるサービスアカウントのキー
を設定してください。

                    (c) TORUPA Laboratory 2019
"""

from os import path, fsync, environ
from urllib.parse import urlparse 
from datetime import datetime, timezone, timedelta

import paho.mqtt.client as mqtt

## 内製のプログラム.
import google_cloud_storage

class MqttClient(mqtt.Client):

    def __init__(self, mqtt_url:str,  bucket_name:str):
        """
        Args
        mqtt_urtl, url in the form like "mqtt://username:password@ip_addr:port"
        bucket_name, bucket name of Google Cloud Storage
        """
        # Make an instance of MQTT client
        super(MqttClient, self).__init__(client_id="", clean_session=True, userdata=None,\
                protocol=mqtt.MQTTv311, transport='tcp')
        self._mqtt_url = mqtt_url
        self._fo = None # file object
        self._bucket_name = bucket_name
        self._prev_time = None


    def on_connect(self, client, userdata, flags, rc):
        '''When MQTT clienct connection established, start subscribing topoics.
        '''
        print("on_connect. ", rc, flags)


    def on_message(self, client, obj, msg):
        """ MQTTメッセージを受信し、データをファイルに出力します。 """
        #print(__name__, 'topic=', msg.topic, ' qos=', str(msg.qos), " payload=", msg.payload)#
        now = datetime.now(self._tz)
        print(self._prev_time.minute, now.minute)
        # If hour is changed, output file name is changed.
        if self._prev_time.hour!= now.hour:
            if self._fo is not None:
                fsync(self._fo.fileno())
                self._fo.close()
                ### storage に upload する
                url = google_cloud_storage.upload_file(self._fo.name, self._bucket_name,
                        "{}{}".format(now.strftime('%Y/%m/%d/'), path.basename(self._fo.name)))
                print( " ({}) file is uploaded from {} to {}".format(__name__, self._fo.name, url))
                self._fo = None
        if self._fo == None:
            filename = '%s.sensor_mqtt.log' % now.strftime('%Y%m%d_%H%M%S')    
            self._fo = open(filename, 'w')
            print(f"open: {filename}  datetime:{now}")
            self._fo.write('date,time,topic,value,\n')
        try:
            self._fo.write("%s,%s,%s,%s,\n"
                 % (now.strftime('%Y/%m/%d'), now.strftime('%H:%M:%S'),
                 msg.topic.split('/')[-1], msg.payload.decode('UTF-8')) )
            self._fo.flush()
            fsync(self._fo.fileno())
            self._prev_time = now
        except Exception as e:
            print(e)


    def on_subscribe(self, client, obj, mid, granted_qos):
        """ MQTT メッセージを受信したときに呼ばれます """
        #print(sys._getframe().f_code.co_name + str(mid) + " " + str(granted_qos))
        pass


    def on_disconnect(self, client, userdata, flag, rc):
        """ MQTTブローカーへの接続を切ったときに呼ばれます """
        if  rc != 0:
            print("Unexpected disconnection.")


    def run(self, topics:list):
        """
        MQTT Client を作成し、run_forever() を実行します。blockingします。
        Args
        ----
        topics, list of string
        """
        self._fo = None
        self._prev_time = datetime.now() - timedelta(days=1)
        self._tz = timezone(timedelta(hours=+9), 'JST')
        self._topics = topics

        url_prs = urlparse(self._mqtt_url)
        print('mqtt://{}:{}@{}{}'.format(url_prs.username, url_prs.password, url_prs.hostname, url_prs.port) )
        #
        if url_prs.username is not None and url_prs.password is not None:
            self.username_pw_set(url_prs.username, url_prs.password)
        self.connect(url_prs.hostname, url_prs.port, 60)
        for tp in topics:
            self.subscribe(tp)
        #self.subscribe("$SYS/#")
        print('loop_forever')
        self.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
        #self.loop_forever()


def test_mqtt_client():
    url_str = environ.get('CLOUDMQTT_KEY')
    mc = MqttClient(url_str, "bucket_name")
    mc.run(topics = ['esp32/pressure', 'esp32/temperature', 'esp32/humidity'])

if __name__ == "__main__":
    test_mqtt_client()
