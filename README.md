# Plugwise custom_component for Home Assistant
A **custom component** to develop an integration monitoring Plugwise Devices, for now only capable of the Anna thermostat.

If you are looking for the **stable, released** version, please upgrade your Home Assistant to 0.98 (released end of August 2019), it is (/will be) part of Home-Assistant now! [Plugwise Component](https://www.home-assistant.io/components/plugwise/)
(while waiting for 0.98 release: [https://github.com/home-assistant/home-assistant.io/blob/next/source/_components/plugwise.markdown](https://github.com/home-assistant/home-assistant.io/blob/next/source/_components/plugwise.markdown))

Currently supports:

- Reading current temperature
- Reading target temperature
- Setting target temperature
- Changing preset_mode 
- Getting scheduled state (and schedules)
- Setting schedule active
- Functional HVAC mode

Todo:

- Adam/Lisa integration
- Ensure async so when timing skews, HA doesn't mention the 'google'-like link mentioned in https://github.com/laetificat/anna-ha/issues/16

**NOTICE**

In readying (before the infamous `climate-1.0` change in HA) this component for upstreaming to the HA project we should rename it to vendor logic. As Plugwise selss more than just climate and we have some community members looking for inclusion of Adam's and Lisa's, changing the name accordingly. For now you can leave your `custom_components/anna` where it is - just create `custom_components/plugwise_dev` and modify your `configuration.yaml` to state `platform: plugwise_dev` (instead of 'platform: anna')

## Installation
- Download release or the master branch as zip
- Verify if you already have a `custom_components` directory (this should be a subdirectory of the directory where `configuration.yaml` resides)
- Extract everything in the `custom_components` directory of this project to your Home Assistant `custom_components` directory

## Usage

Anna should be visible as `climate.plugwise_dev...` in `developer tools` -> `states` 

You can change `preset_mode` using the HASS service call `climate.set_preset_mode` (see below)

You can change the requested temperature using the GUI or HASS service call `climate.set_temperature` (again see below)

## Installing in hass.io (if you are using hass.io on a Raspberry PI or otherwise with hass.io)

Steps:

 - Clone the repo to your local desktop (`git clone` or download and unpack the zip-file).
 - Make sure your favorite editor is loaded as add-on in hass.io (i.e. `https://hassio.local:8123/hassio/store`). Instructions here are using the `IDE` add-on
 - (If you can't get it working, read up on improving security and having certicates, otherwise change the config of `IDE` to include `ssl: false` (instead of `true`)
 - Open the `IDE` page (i.e. `https://hassio.local:8321/`) and confirm your username and password
 - In the directory browser on the left side, verify if you have a `custom_components` directory under `config`. (If so you've done this before so just do what you normally do :))
 - If you haven't, change to the `config` directory - i.e. click it so it's highlighted blue
 - Go to `File` and `Upload local files` in the IDE context menu (top left).
 - Next select ( or drag/drop ) the `custom_components` from the downloaded repository into here
 - Add the `Minimal configuration` indicated below to `configuration.yaml` using the IDE
 - If you go back to the main hass.io interface (i.e. `https://hassio.local:8123`) now, go to configuration->general->validate configuration
 - Also verify the logs using the (i) button of HASS
 - It should say 'Platform not found' on both (which is an error, but because HASS didn't download the modules yet). 
 - Only if it shows the platform not found in the check: continue and go to configuration->general->restart hass from hass
 - After coming up the logs should show something like `1970-01-01 00:00:25 INFO (SyncWorker_34) [homeassistant.loader] Loaded plugwise_dev from custom_components.plugwise_dev`
 - If not, please try restarting again (and or have HASS.io restart the whole system using the HASS.io system tab)

## Configuration

** Please check official documentation on [Plugwise Component](https://www.home-assistant.io/components/plugwise/) as well! **

(while waiting for 0.98 release: [https://github.com/home-assistant/home-assistant.io/blob/next/source/_components/plugwise.markdown](https://github.com/home-assistant/home-assistant.io/blob/next/source/_components/plugwise.markdown))

