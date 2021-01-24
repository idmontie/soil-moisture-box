# Soil Moisture Box

## General Design Goal

```txt
On Raspberry Pi boot, do the following:
    Run this script with forever
        Every 10 seconds, do the following:
            Check soil moisture sensor
                If was wet and now dry AND has not sent message in last day, emit info

On message emit, send a Pushbullet note.
```

## Set up

1. Set up [SSH](https://desertbot.io/blog/ssh-into-pi-zero-over-usb) for your Raspberry pi
2. Copy the `.env.template` to `.env` and add your values.
3. Copy the repo to your pi using `sh ./copy.sh`
4. SSH into the PI `ssh pi@raspberrypi.local`
5. Configure WiFi:

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure
# Wait a few seconds, then verify:
ping google.com
```

6. Install dependencies and test launch script

```bash
# Test the launch script
cd ./soil-moisture-box
bash ./install.sh
bash ./launch.sh
```

7. Add the following to [startup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/):

```sh
sudo systemctl edit --force --full soil.service
 
# Add the folloing
[Unit]
    Description=soil
    Wants=network-online.target
    After=network-online.target
[Service]
    Type=simple
    User=pi
    WorkingDirectory=/home/pi/
    ExecStart=bash ./soil-moisture-box/launch.sh
[Install]
    WantedBy=multi-user.target
 
# Enable the service using:
sudo systemctl enable soil.service
sudo systemctl start soil.service
 
# To check if service ran properly
systemctl status soil
```

8. Reboot

```sh
sudo reboot
```

9. Remember to secure your device using `passwd`.

## Additional Resources

- [TechCoil Reasoing Soil Moisture on MCP3008 chip](https://www.techcoil.com/blog/how-to-read-soil-moisture-level-with-raspberry-pi-and-a-yl-69-fc-28-moisture-sensor/)
