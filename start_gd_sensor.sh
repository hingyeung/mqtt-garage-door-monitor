#!/usr/bin/env bash

set -x

MQTT_SERVER_HOST=ha.corp.lan.samuelli.net
MQTT_SERVER_PORT=1883
DEVICE_UNIQ_ID=garage/garage_door
# DOCKER_IMAGE=mqtt-garage-door-sensor
DOCKER_IMAGE=python3-on-pi-zero-test

docker run --rm --cap-add SYS_RAWIO --device /dev/mem \
  --name ${DOCKER_IMAGE} ${DOCKER_IMAGE} \
  --mqtt-server-host ${MQTT_SERVER_HOST} \
  --mqtt-server-port ${MQTT_SERVER_PORT} \
  --device_uniq_id ${DEVICE_UNIQ_ID}