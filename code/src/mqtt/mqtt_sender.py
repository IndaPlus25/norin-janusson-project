import paho.mqtt.client as mqtt
import json
import os

print("------------")
print("-----" + os.getcwd())


client = mqtt.Client()

client.connect("broker.emqx.io", 1883, 60)

# Get the folder where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the JSON file
file_path = os.path.join(script_dir, "jsonExample.json")
with open(file_path, "r") as f:
    data = json.load(f)

payload = json.dumps(data)

client.publish("test/json", payload)

client.disconnect()
