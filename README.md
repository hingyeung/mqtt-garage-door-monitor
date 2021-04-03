# mqtt-garage-door-monitor

## Setup on Raspberry Pi
1. Install Docker  
`> curl -sSL https://get.docker.com | sh`  
`> sudo systemctl enable docker`  
`> sudo systemctl start docker`  
`> sudo usermod -aG docker pi`  
`> docker --version` 

1. Install bootstrap.sh  
`> cd ${HOME}`  
`> wget https://raw.githubusercontent.com/hingyeung/garage-door-monitor/master/deployer/bootstrap.sh`
`> chmod +x bootstrap.sh`

1. Install systemd script  
`> cd /etc/systemd/system`  
`> wget https://raw.githubusercontent.com/hingyeung/mqtt-garage-door-monitor/master/deployer/mqtt-garage-door-monitor.service`  

1. Modify `garage-door-monitor.service` to replace placeholders: `<IoT_endpoint>`, `<AWS_root_cert_file>`, `<IoT_cert_file>`, `<IoT_cert_private_key_file>`, `<certs_dir>` `additional_mqtt_server_host`, `additional_mqtt_server_port` and `additional_mqtt_topic_prefix`.

1. Start the Garage Door Monitor service  
`> sudo systemctl start garage-door-monitor.service`  

# Delete AWS stack
This script makes sure all previous versions of the Iot policy created by the specified stack are
deleted first, then detach the IoT policy from all IoT certificates, before deleting the stack.  
`> python deployer/delete_stack.py --stack-name ${stack_name}`  

# Attributions
Icons made by [Freepik](https://www.flaticon.com/authors/freepik) from [www.flaticon.com](https://www.flaticon.com/).

## MQTT sample messages
### Create garage door entity in HA using MQTT discovery
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/config" -m '{ "name": "Garage Door", "uniq_id": "garage/garage_door", "stat_t": "homeassistant/binary_sensor/garage/garage_door/state", "qos": 1, "payload_open": "ON", "payload_close": "OFF", "dev_cla": "garage_door", "pl_avail": "online", "pl_not_avail": "offline", "value_template": "{{ value_json.state }}" }'
```

### Manual garage door sensor setup in configuration.yaml
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