import time
import gspread
import pprint

from oauth2client.service_account import ServiceAccountCredentials 

from weather_station import WeatherStation

if __name__ == "__main__":

    print("Connecting to weather station...")

    ws = WeatherStation(device_id='320037000147373336323230', access_token='0a1c7a26974478e675e28e1f97b7e651c4ccf7a1')

    gc = gspread.service_account(filename='client_secret.json')
    sh = gc.open(u"VäderRapport").sheet1

    current_row = 0

    weather_history = []

    while True:

        print("Getting data from sensors...")

        try:
            ws.poll()
        except:
            print("Couldn't contact station...")

        reverse_history = list(reversed(ws.history))

        if len(ws.history) == ws.history_length:
            print("Adding data to google sheets...")
            sh.update("A2:H%d" % (ws.history_length+1), reverse_history)

        time.sleep(15*60.0)
    
