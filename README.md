# Anna component for Home Assistant
A custom component to monitor the Plugwise Anna thermostat in Home Assistant.  
Currently supports:
- Reading current temperature
- Reading target temperature
- Setting target temperature
- Changing hold_mode (i.e. preset)
- Getting scheduled state (and schedules)

## Installation
- Download release or the master branch as zip
- Verify if you already have a `custom_components` directory (this should be a subdirectory of the directory where `configuration.yaml` resides)
- Extract everything in the `custom_components` directory of this project to your Home Assistant `custom_components` directory

## Usage

Anna should be visible as `climate.anna...` in `dev-state` (the `<>` icon in Home Assistant)

You can change `hold_mode` using the HASS service call `climate.set_hold_mode` (see below) - changing it using the GUI is under investigation (how to properly do it)

You can change the requested temperature using the GUI or HASS service call `climate.set_temperature` (again see below)

## Configuration

### Minimal configuration

Update your `configuration.yaml` to contain the below configuration (assuming your smile has `abcdef` on the label and is located at `192.168.1.2`)

```yaml
climate:
  - platform: anna
    password: abcdef
    host: 192.168.1.2
```

### Full configuration option

```yaml
climate:
  - platform: anna
    name: Anna Thermostat   # optional, only if you want to use a different name
    password: your_short_id # required, the ID on the smile (some string of 6 characters)
    host: local_ip_address  # required, the IP-address of your smile
    username: smile         # optional, default username is smile
    port: 80 		    # optional, only needed when other than 80
    scan_interval: 10       # optional, only needed when other than 10
```

## Interacting
 
### Changing temperature

This is done using HASS service `climate.set_temperature` with service data like:

```json
{
  "entity_id": "climate.anna_thermostaat","temperature":19.5
}
```

### Changing hold mode

This is done using HASS service `climate.set_hold_mode` with service data like:

```json
{
  "entity_id": "climate.anna_thermostaat","hold_mode":"away"
}
```

## Debugging

When things don't work out, check your `home-assistant.log` for clues and share them using https://community.home-assistant.io/t/advice-how-to-load-sensor-info-from-plugwise-anna-thermostat-web-interface-xml/87801/60 (or create a GitHub issue). Please first change your `configuration.yaml` to ensure debugging for the Anna component is turned on 

```yaml
logger:
  logs:
    custom_components.anna: debug
```

Example of a working configuration excerpt (with debugging  enabled):

```
[homeassistant.loader] Loaded anna from custom_components.anna
[homeassistant.loader] You are using a custom integration for anna which has not been tested by Home Assistant. This component might cause stability problems, be sure to disable it if you do experience issues with Home Assistant.
[custom_components.anna.climate] Anna: custom component loading (Anna PlugWise climate)
[homeassistant.components.climate] Setting up climate.anna
[custom_components.anna.climate] Anna: Init called
[custom_components.anna.climate] Anna: Initializing API
[custom_components.anna.climate] Anna: platform ready
[custom_components.anna.climate] Anna: Update called
```

Example of something going wrong (IP address not set) excerpt is shown below. Correct your configuration and try again. If the errors persist, please share a larger excerpt of your logfile

```
1970-01-01 00:00:01 ERROR (MainThread) [homeassistant.components.climate] Error while setting up platform anna
  File "/home/homeassistant/.homeassistant/custom_components/anna/climate.py", line 104, in setup_platform
  File "/home/homeassistant/.homeassistant/custom_components/anna/climate.py", line 130, in __init__
    self._api = Haanna(self._username, self._password, self._host, self._port)
```

