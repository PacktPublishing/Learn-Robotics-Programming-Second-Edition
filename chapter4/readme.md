Creating A Headless Pi
======================

This chapter is about making a Raspberry Pi headless, and reaching it from the network.

Using WiFi and SSH
==================

This example wpa_supplicant should be copied onto the BOOT partition of a Raspberry Pi SD card, as wpa_supplicant.conf.
The SSID and PSK will need to be substituted for your own details.

Also an "ssh" file should be present on the SD Card BOOT partition to enable this too.

These will make your Raspberry Pi contactable on your WiFi network.

Contacting The Pi
=================

When it is turned on, the Raspberry Pi will respond on a network to the name "raspberrypi.local" until you change it to a more unique hostname.

You will need to ensure your computer supports MDNS. Most current Linux and Apple Mac desktops already have this support.

## Windows

You will need to install the Apple Bonjour softwarem from https://support.apple.com/downloads/bonjour-for-windows, unless you already have iTunes or Skype installed.