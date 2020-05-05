# -*- coding: utf-8 -*-
"""
センサーロガーのメッセージを受信してファイルに保存するMQTT Client の実装です。

(c) TORUPA Laboratory 2019
"""

import sys
from os import path
import sensor_logger

print("hello")
main_root = path.dirname(path.abspath(__file__))
with open(main_root + "/mqttkey") as f:
    mqtt_url = f.readline()
print("mqtt_url={}".format(mqtt_url))

topics = ['esp32/pressure', 'esp32/temperature', 'esp32/humidity']

mc = sensor_logger.MqttClient(mqtt_url, "mqtt-log-test")
mc.run(topics)

