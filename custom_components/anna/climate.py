"""
Plugwise Anna component for HomeAssistant

configurations.yaml

climate:
  - platform: anna
    name: Anna Thermostat
    username: smile
    password: short_id
    host: 192.168.1.60
    port: 80
    scan_interval: 10
"""

import voluptuous as vol
import logging

import xml.etree.cElementTree as Etree

import haanna

from homeassistant.components.climate import (
    ClimateDevice,
    PLATFORM_SCHEMA)

from homeassistant.components.climate.const import (
    DOMAIN,
    SUPPORT_HOLD_MODE,
    SUPPORT_AWAY_MODE,
    SUPPORT_OPERATION_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    STATE_AUTO,
    STATE_IDLE,
    SERVICE_SET_HOLD_MODE)

from homeassistant.const import (
    CONF_NAME, 
    CONF_HOST, 
    CONF_PORT, 
    CONF_USERNAME, 
    CONF_PASSWORD, 
    TEMP_CELSIUS, 
    ATTR_TEMPERATURE, 
    STATE_ON, 
    STATE_OFF)
import homeassistant.helpers.config_validation as cv

SUPPORT_FLAGS = ( SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE | SUPPORT_HOLD_MODE | SUPPORT_AWAY_MODE )

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:thermometer"

DEFAULT_NAME = 'Anna Thermostat'
DEFAULT_USERNAME = 'smile'
DEFAULT_TIMEOUT = 10
BASE_URL = 'http://{0}:{1}{2}'

# Hold modes
MODE_HOME = "home"
MODE_VACATION = "vacation"
MODE_NO_FROST = "no_frost"
MODE_SLEEP = "asleep"
MODE_AWAY = "away"

# Change defaults to match Anna
DEFAULT_MIN_TEMP = 4
DEFAULT_MAX_TEMP = 30

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=80): cv.string,
    vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Anna thermostat"""
    add_devices([
        ThermostatDevice(
            config.get(CONF_NAME),
            config.get(CONF_USERNAME),
            config.get(CONF_PASSWORD),
            config.get(CONF_HOST),
            config.get(CONF_PORT)
        )
    ])


class ThermostatDevice(ClimateDevice):
    """Representation of an Anna thermostat"""
    def __init__(self, name, username, password, host, port):
        _LOGGER.debug("Init called")
        self._name = name
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._temperature = None
        self._current_temperature = None
        self._outdoor_temperature = None
        self._state = None
        self._hold_mode = None
        self._away_mode = False
        self._operation_list = [ STATE_AUTO, STATE_IDLE ]
        _LOGGER.debug("Initializing API")
        self.update()

    @property
    def should_poll(self):
        """Polling is needed"""
        return True

    @property
    def state(self):
        """Return the current state"""
        return self._state

    def update(self):
        """Update the data from the thermostat"""
        api = haanna.Haanna(self._username, self._password, self._host)
        domain_objects = api.get_domain_objects()
        self._current_temperature = api.get_temperature(domain_objects)
        self._outdoor_temperature = api.get_outdoor_temperature(domain_objects)
        self._temperature = api.get_target_temperature(domain_objects)
        self._hold_mode = api.get_current_preset(domain_objects)
        if api.get_mode(domain_objects) == True:
          self._operation_mode=STATE_AUTO
        else:
          self._operation_mode=STATE_IDLE
        if api.get_heating_status(domain_objects) == True:
          self._state=STATE_ON
        else:
          self._state=STATE_OFF
        _LOGGER.debug("Update called")

    @property
    def name(self):
        return self._name

    @property
    def current_hold_mode(self):
        """Return the current hold mode, e.g., home, away, temp."""
        return self._hold_mode

    @property
    def operation_list(self):
        """Return the operation modes list."""
        return self._operation_list

    @property
    def current_operation(self):
        """Return current operation ie. auto, idle."""
        return self._operation_mode

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._temperature

    @property
    def outdoor_temperature(self):
        return self._outdoor_temperature

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    def set_temperature(self, **kwargs):
        """Set new target temperature"""
        import haanna
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            api = haanna.Haanna(self._username, self._password, self._host)
            self._temperature = temperature
            domain_objects = api.get_domain_objects()
            api.set_temperature(domain_objects, temperature)
            self.schedule_update_ha_state()

    def set_hold_mode(self, hold_mode):
        """Set the hold mode."""
        if hold_mode is not None:
            api = haanna.Haanna(self._username, self._password, self._host)
            domain_objects = api.get_domain_objects()
            self._hold_mode = hold_mode
            api.set_preset(domain_objects, hold_mode)
            _LOGGER.info('Changing hold mode/preset')
        else:
            _LOGGER.error('Failed to change hold mode (invalid preset)')

