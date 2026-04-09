import paho.mqtt.client as mqtt
import json

client = mqtt.Client()

client.connect("broker.emqx.io", 1883, 60)

data = {
    "temperature": 25.5,
    "humidity": 60
}

payload = json.dumps(data)  # convert dict → JSON string

client.publish("test/json", payload)

client.disconnect()