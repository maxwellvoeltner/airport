import config
import requests
from utils import timing_aux
from airsimDFA import Airsim

# functions that help set up the simulation

# clears out the airplane collection and puts in the airplanes from the config file
def reset_airplane_database():
    # deleting original airplanes
    delete_response = requests.delete(config.airplanes_api_url, headers=config.api_headers)

    if delete_response.status_code != 200:
        return

    # inserting new airplanes from initial config
    for airplane in config.initial_airplanes:
        create_response = requests.post(config.airplanes_api_url, json=airplane, headers=config.api_headers)

        if create_response.status_code == 200:
            print(f"Added airplane: {airplane['sourceAirport']}")
        else:
            print(f"Failed to add {airplane['sourceAirport']}: {create_response.json()}")


# gets a list of sourceAirports of the flights which will be used as flight_id's by the state machine
def get_airplane_id_list():

    # Making the GET request
    airplanes = requests.get(config.airplanes_api_url, headers=config.api_headers)
    airplanes = airplanes.json()

    # getting list of airplane names in order
    airplane_ids = [airplane.get("sourceAirport") for airplane in airplanes]
    print(airplane_ids)

    return airplane_ids


def sync_departure_times( mode ):
    # Modify the original list in-place
    timing = timing_aux.calculate_timing( config.state_minimum_loops[mode] )
    relative_arrival_time = timing.get("time_to_arrive")
    relative_departure_time = timing.get("time_to_depart")
    for airplane in config.initial_airplanes:
        airplane["departureTime"] = ((airplane["arrivalTime"] -  relative_arrival_time) + relative_departure_time)


def initialize_statemachine( mode, flight_id_list, alcms_client, fuel_client, gate_client):
    # getting either demo state times or competition state times based on the mode
    times = config.state_minimum_loops.get(mode)
    timing = timing_aux.calculate_timing(times)
    timing_aux.print_startup_summary(mode, timing)

    return Airsim(
        mode=mode,
        alcms_client=alcms_client,
        fuel_client=fuel_client,
        gate_client=gate_client,
        starting_minutes=timing["start_time"],
        minutes_per_loop=timing["minutes_per_loop"],
        time_to_arrive_from_s0=timing["time_to_arrive_from_state_zero"],
        flight_list=flight_id_list,
        **times
    )