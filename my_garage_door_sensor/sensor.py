from homeassistant.components.binary_sensor import DEVICE_CLASS_GARAGE_DOOR, BinarySensorEntity

class MyGarageDoorSensor(BinarySensorEntity):
  @property
  def is_on(self):
    """Return true if the binary sensor is on."""
    return True

  @property
  def state(self):
    """Return the state of the binary sensor."""
    return is_on

  @property
  def device_class(self):
    """Return the class of this device, from component DEVICE_CLASSES."""
    return DEVICE_CLASS_GARAGE_DOOR
  