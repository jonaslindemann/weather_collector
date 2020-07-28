import os, datetime, json

from pyparticle import Particle

class WeatherStation:
    def __init__(self, device_id, access_token):

        self.__token = access_token
        self.__device_id = device_id

        self.__particle = Particle(access_token=access_token)

        self.history_length = 96
        self.history = []

        self.windspeed_ms = 0.0
        self.windgust_ms = 0.0
        self.wind_direction = 0.0
        self.humidity = 0.0
        self.temp_C = 0.0
        self.rain = 0.0
        self.daily_rain = 0.0

        self.latest_poll = datetime.datetime.now()

        self.history_filename = "ws-state.json"

        self.load_from_json()

    def load_from_json(self):

        if os.path.exists(self.history_filename):
            with open(self.history_filename, "r") as state_file:
                self.history = json.load(state_file)
        else:
            self.fill_table()
            self.save_to_json()

    def save_to_json(self):

        with open(self.history_filename, "w") as state_file:
            json.dump(self.history, state_file)

    def fill_table(self):

        self.history.clear()

        for i in range(self.history_length):
            self.history.append(self.get_row())
        
    def poll(self):

        self.windspeed_ms = self.__particle.get_variable(self.__device_id, "windspeedms")["result"]
        self.windgust_ms = self.__particle.get_variable(self.__device_id, "windgustms")["result"]
        self.wind_direction = self.__particle.get_variable(self.__device_id, "winddir")["result"]
        self.humidity = self.__particle.get_variable(self.__device_id, "humidity")["result"]
        self.temp_C = self.__particle.get_variable(self.__device_id, "tempC")["result"]
        self.rain = self.__particle.get_variable(self.__device_id, "rainin")["result"]
        self.daily_rain = self.__particle.get_variable(self.__device_id, "dailyrainin")["result"]

        self.latest_poll = datetime.datetime.now()

        self.history.append(self.get_row())
        if len(self.history)>self.history_length:
            self.history.remove(self.history[0])

        self.save_to_json()

    def get_row(self):
        return [str(self.latest_poll), self.humidity, self.temp_C, self.rain, self.daily_rain, self.wind_direction, self.windspeed_ms, self.windgust_ms]

    def __str__(self):
        table_str = ""
        for row in self.history:
            table_str += "{:s} {:10.3g} {:10.3g} {:10.3g} {:10.3g} {:10.3g} {:10.3g} {:10.3g}\n".format(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])

        return table_str
