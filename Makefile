INTEGRATION_NAME:=my_garage_door_sensor
INTEGATION_DIR:=ha_config/custom_components/${INTEGRATION_NAME}

deploy:
	rm -r ${INTEGATION_DIR}
	mkdir -p ${INTEGATION_DIR}
	cp ${INTEGRATION_NAME}.py ${INTEGATION_DIR}/
	docker-compose restart homeassistant-garage-door-test