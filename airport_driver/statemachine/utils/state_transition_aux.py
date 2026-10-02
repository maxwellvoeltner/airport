import requests
import config
from utils import airport_io

# on enter and on exit function helpers

# gets the flight_objects by the unique sourceAirport attribute of the flight from the flight collection
def get_airplane(source_airport):

    # Making the GET request
    airplane = requests.get(f"{config.airplanes_api_url}{source_airport}", headers=config.api_headers)
    airplane = airplane.json()

    return airplane


# updates current flight with new data established by state transition
def update_flight(sourceAirport, data):

    # just abstracts the long request line from each function it's called in
    res = requests.patch(f'{config.airplanes_api_url}{sourceAirport}', json=data, headers=config.api_headers)


# resetting the flights
def reset_airplanes():

    batch_reset = []

    for airplane_object in config.initial_airplanes:

        # getting the source airport (identifier)
        sourceAirport = airplane_object.get("sourceAirport")
        # add airplane object to the update list
        batch_reset.append({
            "sourceAirport": sourceAirport,
            "update": airplane_object
        })

    res = requests.patch(f'{config.airplanes_api_url}batch', json=batch_reset, headers=config.api_headers)

    if res.status_code == 200:
        print("Reset Airplanes")
    else:
        print("Could not reset airplanes")


def set_signal(mode, alcms_client, day, component_name, action, day_only=False):

    if (mode == "competition") or (day_only and day == 0):
        return
    
    if component_name == "RW6L":
        airport_io.write_RW6L(alcms_client, action)

    elif component_name == "RW6R":
        airport_io.write_RW6R(alcms_client, action)

    elif component_name == "taxiway_lights":
        airport_io.write_taxiway_lights(alcms_client, action)