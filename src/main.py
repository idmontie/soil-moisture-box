from dotenv import Dotenv
from gpiozero import DigitalInputDevice
from pushbullet import Pushbullet
from datetime import datetime, timedelta
from time import sleep
import os

dotenv = Dotenv('.env')

HUMIDITY_PIN = int(dotenv['HUMIDITY_PIN'])
MESSAGE_INTERVAL_HOURS = int(dotenv['MESSAGE_INTERVAL_HOURS'])
LOOP_INTERVAL = int(dotenv['LOOP_INTERVAL'])
digital_input = None
current_soil = False
last_message_sent = datetime.now() - timedelta(hours=MESSAGE_INTERVAL_HOURS)

pb = Pushbullet(dotenv['PUSHBULLET_API_KEY'])

def init_pins():
    global digital_input, HUMIDITY_PIN
    digital_input = DigitalInputDevice(HUMIDITY_PIN)

def is_soil_humid():
    '''
    Returns true (digital input is low) if the soil is wet
    Returns false (gitial input is high) if the soil is dry
    '''
    global digital_input
    return not digital_input.value

def emit_message():
    print('water your plants')
    pb.push_note("Water Your Plants!", "Looks like its time to water the plants.")

def loop():
    global current_soil, last_message_sent, MESSAGE_INTERVAL_HOURS
    # TODO remind the user to change the battery

    next_soil = is_soil_humid()

    if (current_soil != next_soil and not next_soil):
        now = datetime.now()
        difference = now - last_message_sent
        should_send_message = difference.total_seconds() > MESSAGE_INTERVAL_HOURS * 60 * 60

        if (should_send_message):
            emit_message()
            last_message_sent = datetime.now()
    
    current_soil = next_soil
    
def main():
    global LOOP_INTERVAL

    init_pins()

    while (True):
        loop()
        sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main()
