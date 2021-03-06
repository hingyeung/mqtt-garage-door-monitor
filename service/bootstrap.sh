#!/usr/bin/env bash
set -e
# run this script from /etc/systemd/system/mqtt-garage-door-monitor.service

MQTT_SERVER_HOST=$1
MQTT_SERVER_PORT=$2
MQTT_USERNAME=$3
MQTT_PASSWORD=$4
MQTT_DEVICE_UNIQ_ID=$5

PROJECT_DIR=mqtt-garage-door-monitor
DOCKER_IMAGE=mqtt-garage-door-monitor

echo "Checking if ${PROJECT_DIR} exists..."
if [ ! -d "${HOME}/${PROJECT_DIR}" ]
then
  echo "${PROJECT_DIR} does not exist. Cloning..."
  git clone https://github.com/hingyeung/mqtt-garage-door-monitor.git
  cd ${PROJECT_DIR}
else
  echo "${PROJECT_DIR} exists, updating..."
  cd ${PROJECT_DIR}
  git pull
fi

echo "Building Docker image ${DOCKER_IMAGE}"
cd mqtt_garage_door_monitor
docker build -t ${DOCKER_IMAGE} .

echo "Running Docker image ${DOCKER_IMAGE}"
# https://bit.ly/2OiWBtR
docker run --rm --cap-add SYS_RAWIO --device /dev/mem \
  -v /etc/localtime:/etc/localtime:ro \
  --name ${DOCKER_IMAGE} \
  ${DOCKER_IMAGE} \
  --mqtt-server-host ${MQTT_SERVER_HOST} \
  --mqtt-server-port ${MQTT_SERVER_PORT} \
  --mqtt-username ${MQTT_USERNAME} \
  --mqtt-password ${MQTT_PASSWORD} \
  --device_uniq_id ${MQTT_DEVICE_UNIQ_ID}
