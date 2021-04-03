from homeassistant.components.binary_sensor import DEVICE_CLASS_GARAGE_DOOR, BinarySensorEntity

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([MyGarageDoorSensor()])

class MyGarageDoorSensor(BinarySensorEntity):
  @property
  def name(self):
    """Return the name of the sensor."""
    return 'My Garage Door Monitor'

  @property
  def is_on(self):
    """Return true if the binary sensor is on."""
    return True

  @property
  def device_class(self):
    """Return the class of this device, from component DEVICE_CLASSES."""
    return DEVICE_CLASS_GARAGE_DOOR
  