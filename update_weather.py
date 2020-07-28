# -*- coding: utf-8 -*-

import time
import gspread
import sys
import configparser as cp

from oauth2client.service_account import ServiceAccountCredentials 

from weather_station import WeatherStation

if __name__ == "__main__":

    print('Reading configuration')

    config = cp.ConfigParser()
    config.read('/etc/weather_collector.conf')

    device_id = -1
    access_token = -1
    client_secret_filename = ''
    polling_interval = 15
    state_filename = ''

    if config.has_option('particle', 'device_id'):
        device_id = config['particle']['device_id']
    if config.has_option('particle', 'access_token'):
        access_token = config['particle']['access_token']
    if config.has_option('gspread', 'client_secret'):
        client_secret_filename = config['gspread']['client_secret']
    if config.has_option('general', 'polling_interval'):
        polling_interval = int(config['general']['polling_interval'])
    if config.has_option('general', 'state_filename'):
        state_filename = config['general']['state_filename']

    if (device_id == -1) or (access_token == -1) or (client_secret_filename == ''):
        print('Missing configuration parameters.')
        sys.exit(-1)
    
    print('Connecting to weather station...')

    ws = WeatherStation(device_id=device_id, access_token=access_token, history_filename=state_filename)

    try:
        gc = gspread.service_account(filename=client_secret_filename)
        sh = gc.open(u'VäderRapport').sheet1
    except:
        print('Couldn\'t open gspread document.')
        sys.exit(-1)

    while True:

        print('Getting data from sensors...')

        try:
            ws.poll()
        except:
            print('Couldn\'t contact station...')

        reverse_history = list(reversed(ws.history))

        if len(ws.history) == ws.history_length:
            print('Adding data to google sheets...')

            try:
                sh.update('A2:H%d' % (ws.history_length+1), reverse_history)
            except:
                print('Couldn\'t update google document.')

        print('Sleeping...')

        time.sleep(polling_interval*60)
    
