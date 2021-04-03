# mqtt-garage-door-monitor

## Create garage door entity in HA using MQTT discovery
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/config" -m '{ "name": "Garage Door", "uniq_id": "garage/garage_door", "stat_t": "homeassistant/binary_sensor/garage/garage_door/state", "qos": 1, "payload_open": "ON", "payload_close": "OFF", "dev_cla": "garage_door", "pl_avail": "online", "pl_not_avail": "offline", "value_template": "{{ value_json.state }}" }'
```

## Manual garage door sensor setup in configuration.yaml
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
    # birth_message:
    #   topic: "homeassistant/binary_sensor/garage/garage_door/availability"
    #   payload: "online"
    # will_message:
    #   topic: "homeassistant/binary_sensor/garage/garage_door/availability"
    #   payload: "offline"
```

## Garage door closed
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/state" -m 'OFF'
```

## Garage door opened
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/state" -m 'ON'
```

## Garage door available
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/availability" -m
'online'
```

## Garage door not available
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/availability" -m
'offline'
```

## Delete garage door entity previously created using MQTT discovery
```bash
/usr/bin/mosquitto_pub -h 192.168.1.129 -p 1883 -t "homeassistant/binary_sensor/garage/garage_door/config" -m ''
```