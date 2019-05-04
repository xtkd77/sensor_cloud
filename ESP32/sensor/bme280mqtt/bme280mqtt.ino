/* This program read BME280 sensor data, upload the data as MQTT client to MQTT broker.
* User have to prepare followings:
* (1) WiFi connection: SSID and passsword
* (2) MQTT connection: broker URL, port number, user name, password
* These information must be set in this program.
*/
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BME280.h>

#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "";
const char* password = "";
WiFiClient espClient;

// Add your MQTT Broker IP address, example:
const char* usrname = "";
const char* passwd = "";

PubSubClient client(espClient);

/// SPI pin asignment
#define BME_SCK 14
#define BME_MISO 12
#define BME_MOSI 13
#define BME_CS 15
Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK);

#define SEALEVELPRESSURE_HPA (1013.25)

void setup() {
    Serial.begin(9600);
    Serial.println(F("BME280 test"));

    bool status = bme.begin();
    if (!status) {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
        while (1);
    }

    Serial.println("-- Default Test --");
    Serial.println();

    /* connect to WIFi in the room */
    setup_wifi();
    /* connect MQTT client to broker  */
    client.setServer("", 0);/*!!! SET URL and port number !!! */
    //client.setCallback(callback);
}

void callback(char* topic, byte* message, unsigned int length) {
  ;
}
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);  Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client",usrname, passwd)) {
      Serial.println("connected");
      // Subscribe
      //client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    delay(1000);
    char tempString[8];
    float temperature = bme.readTemperature();
    dtostrf(temperature, 1, 2, tempString);
    client.publish("esp32/temperature", tempString);

    float prs = bme.readPressure() / 100.0F;
    dtostrf(prs, 1, 2, tempString);
    client.publish("esp32/pressure", tempString);

    float hmd = bme.readHumidity();
    dtostrf(hmd, 1, 2, tempString);
    client.publish("esp32/humidity", tempString);
}
