# mqtt-garage-door-monitor

## Setup on Raspberry Pi
1. Install Docker  
```bash
curl -sSL https://get.docker.com | sh 
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker pi
docker --version
```

1. Install bootstrap.sh  
```bash
cd ${HOME}
wget https://raw.githubusercontent.com/hingyeung/mqtt-garage-door-monitor/main/service/bootstrap.sh
chmod +x bootstrap.sh
```

1. Install systemd script  
    ```bash
    cd /etc/systemd/system
    wget https://raw.githubusercontent.com/hingyeung/mqtt-garage-door-monitor/main/service/mqtt-garage-door-monitor.service
    ```
1. Modify `mqtt-garage-door-monitor.service` to replace placeholders: `mqtt_server_host`, `mqtt_server_port` and `device_uniq_id`.
1. Start the Garage Door Monitor service
    ```bash
    sudo systemctl start mqtt-garage-door-monitor.service
    ```
1. Start the Garage Door Monitor service on boot
    ```bash
    sudo systemctl enable mqtt-garage-door-monitor.service
    ```

## Manual garage door sensor setup in Home Assistant's configuration.yaml
```yaml
binary_sensor:
  - platform: mqtt
    name: "Garage Door"
    unique_id: "garage_door"
    state_topic: "homeassistant/binary_sensor/garage/garage_door/state"
    payload_on: "ON"
    availability:
      - topic: "homeassistant/binary_sensor/garage/garage_door/availability"
        payload_available: "online"
        payload_not_available: "offline"
    qos: 0
    device_class: garage_door
```

## Running local Home Assistant for integration testing
```bash
cd local-ha
./start_ha.sh
#
# do your testing
#
./stop_ha.sh
```

## MQTT sample messages
### Starting a shell with Mqsquitto client pre-installed
```bash
cd local_ha
./start_mqtt_shell.sh
```
You can now send MQTT message to your broker using `mosquitto_pub`.

### Create garage door entity in HA using MQTT discovery
If you don't want to manually setup you garage door monitor in HA's configuration.yaml, you can use the following MQTT message to setup the monitor.
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/config" -m '{ "name": "Garage Door", "uniq_id": "garage/garage_door", "stat_t": "homeassistant/binary_sensor/garage/garage_door/state", "qos": 1, "payload_open": "ON", "payload_close": "OFF", "dev_cla": "garage_door", "pl_avail": "online", "pl_not_avail": "offline", "value_template": "{{ value_json.state }}" }'
```

### Garage door closed
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/state" -m 'OFF'
```

### Garage door opened
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/state" -m 'ON'
```

### Garage door available
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/availability" -m
'online'
```

### Garage door not available
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/availability" -m
'offline'
```

### Delete garage door entity previously created using MQTT discovery
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/config" -m ''
```