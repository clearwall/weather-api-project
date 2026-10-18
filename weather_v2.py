import os
import requests
import json


class City:
    def __init__(self, lat, lon, units="metric"):
        self.lat = lat
        self.lon = lon
        self.units = units

    def get_data(self):
        api_key = os.environ["OPENWEATHER_API_KEY"]

        params = {
            "units": self.units,
            "lat": self.lat,
            "lon": self.lon,
            "appid": api_key
        }

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params=params
            )

            response.raise_for_status()
        except requests.exceptions.SSLError as error:
            print("The secure connection could not be verified.")
            print(error)
            return False

        except requests.exceptions.ConnectionError as e:
            print("Oops! No internet access, please connect to a network and retry.")
            print(e)
            return False

        except requests.exceptions.RequestException as e:
            print("Oops! Something went wrong with the API request.")
            print(e)
            return False

        response_json = response.json()
        #print(json.dumps(response_json, indent=4))

        self.name = response_json["name"]
        self.temp = response_json["main"]["temp"]
        self.temp_min = response_json["main"]["temp_min"]
        self.temp_max = response_json["main"]["temp_max"]

        return True

    def temp_print(self):
        if self.units == "imperial":
            temp_symbol = "°F"
        else:
            temp_symbol = "°C"

        print()
        print(f"In {self.name} it is currently {self.temp}{temp_symbol}")
        print(f"Current Maximum: {self.temp_max}{temp_symbol}")
        print(f"Current Minimum: {self.temp_min}{temp_symbol}")
        print()


# Preset coordinates
home = (-31.95, 115.85)
vacation = (-8.7233, 115.1723)


print("Weather Lookup")
print()
print("1. Home")
print("2. Vacation")
print("3. Custom")
print()

selection = input("Please select an option: ")


if selection == "1":
    city = City(home[0], home[1])

elif selection == "2":
    city = City(vacation[0], vacation[1])

elif selection == "3":
    try:
        lat = float(input("Enter latitude: "))
        lon = float(input("Enter longitude: "))

        units_input = input(
            "Select units - M for Metric or I for Imperial [default: M]: "
        ).strip().upper()

        if units_input == "" or units_input == "M":
            units = "metric"

        elif units_input == "I":
            units = "imperial"

        else:
            print("Invalid selection. Please enter M or I.")
            exit()

        city = City(lat, lon, units)

    except ValueError:
        print("Latitude and longitude must be numbers.")
        exit()

else:
    print("Invalid selection.")
    exit()


if city.get_data():
    city.temp_print()