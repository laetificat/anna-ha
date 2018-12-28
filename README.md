# Anna component for Home Assistant
A custom component to monitor the Plugwise Anna thermostat in Home Assistant.  
Currently supports:
- Reading current temperature
- Reading target temperature
- Setting target temperature

## Installation
- Download release or the master branch as zip
- Extract everything in custom_components directory to your Home Assistant custom_components directory

## Configuration
```yaml
climate:
  - platform: anna
    name: Anna Thermostat
    username: smile
    password: your_short_id
    host: local_ip_address
    port: port_number
    scan_interval: 10
```
