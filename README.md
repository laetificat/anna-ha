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
- Extract everything in custom_components directory to your Home Assistant custom_components directory

## Configuration
```yaml
climate:
  - platform: anna
    name: Anna Thermostat   # optional, only if you want to use a different name
    username: smile         # optional, default username is smile
    password: your_short_id
    host: local_ip_address
    port: port_number       # optional, only needed when other than 80
    scan_interval: 10       # optional, only needed when other than 10
```

## Changing hold_mode

This is done using HASS service `climate.set_hold_mode` with service data like:

```json
{
  "entity_id": "climate.anna_thermostaat","hold_mode":"away"
}
```
