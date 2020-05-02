# -*- coding: utf-8 -*-
"""

センサーロガーのメッセージを受信してファイルに保存するMQTT Client の実装です。

(c) TORUPA Laboratory 2019

"""

import sys, os
import urllib.parse as urlparse
import paho.mqtt.client as mqtt
import socket, select
import datetime

import gcp_pubsub # Google PubSub を利用するためのmodule

gcp_pubsub.initialize()

mqtt_url = sys.argv[1] # e.g., "mqtt://username:password@ip_addr:port"

topics = ['esp32/pressure', 'esp32/temperature', 'esp32/humidity']
url_str = os.environ.get('CLOUDMQTT_URL', mqtt_url)


#
# Make an instance of MQTT client
#
#mqttc = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport='tcp')
mqttc = mqtt.Client("", True, None, mqtt.MQTTv31)

#
# Parse CLOUDMQTT_URL
#
url_prs = urlparse.urlparse(url_str)
print('mqtt://{}:{}@{}{}'.format(url_prs.username, url_prs.password, url_prs.hostname, url_prs.port) )

fo = None
prev_hour = -1
tz = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

#############################################################################
def on_connect(client, userdata, flags, rc):
    '''When MQTT clienct connection established, start subscribing
    topoics.
    '''
    if rc == 0:
        for t in topics:
            print(t)
            client.subscribe(t)
    else:
        print(sys._getframe().f_code.co_name, "rc != 0")


def on_message(client, obj, msg):
    """ MQTTメッセージを受信し、データをファイルに出力します。 """

    #print(sys._getframe().f_code.co_name)        
    print(__name__, 'topic=', msg.topic, ' qos=', str(msg.qos), " payload=", msg.payload)
    now = datetime.datetime.now(tz)

    # If hour is changed, output file name is changed.
    global prev_hour
    global fo
    if prev_hour != now.hour:
        if fo is not None:
            fo.close()
        fo = None
    if fo == None:
        filename = '%s.sensor_mqtt.log' % now.strftime('%Y%m%d_%H%M%S')    
        fo = open(filename, 'w')
        print(f"open: {filename}  datetime:{now}")
        fo.write('date,time,topic,value,\n')
    fo.write("%s,%s,%s,%s,\n"
             % (now.strftime('%Y/%m/%d'), now.strftime('%H:%M:%S'),
                 msg.topic.split('/')[-1], msg.payload.decode('UTF-8')) )
    fo.flush()
    os.fsync(fo.fileno())
    try:
        gcp_pubsub.publish_msg("mydevice",  msg.payload)
    except Exception as e:
        print(e)
        pass
    #
    prev_hour = now.hour


def on_subscribe(client, obj, mid, granted_qos):
    """ MQTT メッセージを受信したときに呼ばれます """

    print(sys._getframe().f_code.co_name)        
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_disconnect(client, userdata, flag, rc):
    """ MQTTブローカーへの接続を切ったときに呼ばれます """

    if  rc != 0:
        print("Unexpected disconnection.")


#############################################################################
#
# Set MQTT event callbacks and connect
#
mqttc.on_message = on_message
mqttc.on_connect = on_connect # start subscription 
mqttc.on_disconnect = on_disconnect

if url_prs.username is not None and url_prs.password is not None:
    mqttc.username_pw_set(url_prs.username, url_prs.password)
mqttc.connect(url_prs.hostname, url_prs.port, 60)
print('loop_forever')
mqttc.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)

#############################################################################
