import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)  # JSON string → dict

    print("Received:", data)
    print("Temperature:", data["temperature"])

client = mqtt.Client()
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)
client.subscribe("test/json")

client.loop_forever()