#!/usr/bin/env python

import RPi.GPIO as io
import time
import logging
import paho.mqtt.client as mqtt
import argparse
import json

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# https://github.com/home-assistant/example-custom-config/tree/master/custom_components/example_sensor
DOOR_PIN = 24
STATE_ON = "ON"
STATE_OFF = "OFF"
STATE_DESC_MAP = {STATE_ON: "OPENED", STATE_OFF: "CLOSED"}

def setup_door_sensor():
    io.setmode(io.BCM)
    io.setup(DOOR_PIN, io.IN, pull_up_down=io.PUD_UP)


def getSerial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


def getClientId():
    return 'MQTTGarageDoorMonitor-' + getSerial()


def get_config_topic(device_uniq_id):
    return f'homeassistant/binary_sensor/{device_uniq_id}/config'


def get_state_topic(device_uniq_id):
    return f"homeassistant/binary_sensor/{device_uniq_id}/state"

def get_availability_topic(device_uniq_id):
    return f"homeassistant/binary_sensor/{device_uniq_id}/availability"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", action="store", dest="interval", default=1,
                        help="Time between polling door status (second)")
    parser.add_argument("--mqtt-server-host", action="store", dest="mqtt_server_host",
                        help="MQTT Server Host", default="localhost")
    parser.add_argument("--mqtt-server-port", action="store", dest="mqtt_server_port",
                        help="MQTT Server Port", default=1883, type=int)
    parser.add_argument("--device_uniq_id", action="store", dest="device_uniq_id",
                        help="Device unique ID", default="garage/garage_door")

    args = parser.parse_args()

    return (
        args.interval,
        args.mqtt_server_host,
        args.mqtt_server_port,
        args.device_uniq_id
    )

def on_connect(client, userdata, flags, rc):
    device_id = userdata
    logger.info("{} connected with result code: {}".format(device_id, rc))
    send_birth_message(client, device_id)

def on_disconnect(client, userdata, rc=0):
    logger.info("Disconnected result code "+str(rc))

def create_mqtt_client(host, port, device_uniq_id):
    client = mqtt.Client(client_id=getClientId(), userdata=device_uniq_id)

    # set up last will before connecting
    client.will_set(
        get_availability_topic(device_uniq_id), 'offline', 1, True
    )
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host, port=port)
    return client


def send_config_message(client, device_uniq_id):
    message = {
        "name": "Garage Door", "uniq_id": device_uniq_id, "stat_t": get_state_topic(device_uniq_id),
        "qos": 1, "payload_on": "closed", "payload_off": "opened", "dev_cla": "garage_door"
    }
    client.publish(get_config_topic(device_uniq_id), json.dumps(message), 0)

def send_birth_message(mqtt_client, device_uniq_id):
    mqtt_client.publish(
        get_availability_topic(device_uniq_id), 'online', 1, True
    )

def main():
    (interval, mqtt_host, mqtt_port, device_uniq_id) = parse_args()
    mqtt_client = create_mqtt_client(mqtt_host, mqtt_port, device_uniq_id)
    
    # using manual setup in configuration.yaml
    # send_config_message(mqtt_client, device_uniq_id)

    setup_door_sensor()

    prev_state = str(None)
    mqtt_client.loop_start()

    # send birth message
    send_birth_message(mqtt_client, device_uniq_id)

    while True:
        # Be consistent with HA binary sensor standard
        # On means open, Off means closed.
        # https://developers.home-assistant.io/docs/core/entity/binary-sensor
        # message = {"clientId": getClientId()}
        if io.input(DOOR_PIN):
            current_state = STATE_ON
        else:
            current_state = STATE_OFF

        logger.debug("current state: {}".format(current_state))

        if prev_state != current_state:
            logger.info("state changed from {} to {} (state: {})".format(
                prev_state, current_state, STATE_DESC_MAP.get(current_state))
            )

            prev_state = current_state

            mqtt_client.publish(
                get_state_topic(device_uniq_id), current_state
            )

        time.sleep(interval)


if __name__ == "__main__":
    main()
