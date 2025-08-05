import config
import requests


def state_name_to_index( state_name ):
    '''
    Description:
        turns the english word of a number into the integer value of the number

    Parameters:
        state_name (str) -> the name of the state

    Returns:
        word_to_num[key] (int) -> the numerical representation of the state name
    '''
    # mapping of state names to numbers
    word_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19, "twenty": 20, "twenty_one": 21,
        "twenty_two": 22, "twenty_three": 23, "twenty_four": 24,
        "twenty_five": None, "twenty_six": None, "twenty_seven": None,
        "twenty_eight": None
    }

    # splits the state name into substrings by the underscore and gets the last one ( which is the position of the english version of the number of the state )
    key = state_name.split("_", 1)[-1]
    # returns the mapped number to that english version of the number of the state
    return word_to_num[key]


def calculate_uninterrupted_time( sm, destination_state ):
    '''
    Description:
        calculates the minimum amount of sim time ( no delays ) it would take for the state machine to reach another state from where it is now

    Parameters:
        sm (Airsim(StateMachine)) -> the state machine that controls the state of the airplane
        destination_state (str) -> one of the following: "next_flight_arrival", "current_flight_arrival", "current_flight_departure"

    Returns:
        (remaining_loops * sm.minutes_per_loop) (float) -> the amount of sim time it takes for the state machine to get to the destination state uninterrupted from where it is now
    '''

    # initialization
    state_name = sm.current_state.name
    current_idx = 0
    extra_wait_loops = 0

    # getting the numerical value of the state
    current_idx = state_name_to_index( state_name )

    if current_idx is None: # holding state - no extra wait
        current_idx = 2  # as if we're about to enter state_3 from state 2
    else:
        # find out how many more loops are needed to stay in current state before a transition is possible
        time_in_current_state = sm.loop_num - sm.state_entry_loop_num
        current_min_required = getattr(sm, f"s{current_idx}_min")
        extra_wait_loops = max(0, current_min_required - time_in_current_state)

    # initializing our accumulator with the extra wait loops in the current state
    remaining_loops = extra_wait_loops

    # calculating uninterrupted time needed until the next flight's arrival
    if destination_state == "next_flight_arrival":
        # add loops for current flight states (current state -> state_twenty_four)
        for i in range(current_idx + 1, 25):
            remaining_loops += getattr(sm, f"s{i}_min")
        # add loops for the next flight states (state_zero to state_six)
        for i in range(7):
            remaining_loops += getattr(sm, f"s{i}_min")

    # calculating uninterrupted time until the current flight's arrival
    elif destination_state == "current_flight_arrival":
        # add loops for current flight states (current state -> state_six)
        for i in range(current_idx + 1, 7):
            remaining_loops += getattr(sm, f"s{i}_min")

    # calculating uninterrupted time until the current flight's departure
    elif destination_state == "current_flight_departure":
        # add loops for current flight states (current state -> state_six)
        for i in range(current_idx + 1, 23):
            remaining_loops += getattr(sm, f"s{i}_min")

    # returning uninterrupted time by multiplying uninterrupted loops by minutes per loop
    return (remaining_loops * sm.minutes_per_loop)


def delay_flights( sm ):
    '''
    Description:
        delays current flight and subsequent flights if necessary

    Parameters:
        sm (Airsim(StateMachine)) -> the state machine that controls the state of the airplane

    Returns:
        None (just updates the flights with delays)
    '''
    print("entered delay function")

    # Get all airplanes and map them by sourceAirport
    airplanes = requests.get(config.airplanes_api_url, headers=config.api_headers).json()
    # create a dictionary mapping the source airport to its airplane object
    airplanes = {plane.get("sourceAirport"): plane for plane in airplanes}

    # initializations
    flight_list = sm.flight_list
    current_time = sm.simulation_minutes
    batch_update = []

    # calculating uninterrupted time needed for next flight to arrive from current state
    next_flight_arrival_uninterrupted_time_needed = calculate_uninterrupted_time(sm, "next_flight_arrival")
    previous_flight_arrival_time = -1
    # starting delay offset
    delay_offset = 0

    # cycling through upcoming flights in order
    for i in range(sm.current_flight_index, len(flight_list)):
        # getting the name and airplane object
        flight_name = flight_list[i]
        airplane = airplanes[flight_name]

        # the first flight is the current flight and that gets handled separately here
        if i == sm.current_flight_index:

            # if the airplane hasn't arrived yet
            if not (airplane.get("arrivalStatus") == "Arrived"):

                # calculate how much time there is between now and when the plane is scheduled to arrive
                arrival_time = float(airplane["arrivalTime"])
                gap = arrival_time - current_time

                # calculate how much time is needed for the state machine to get to the landing state
                uninterrupted_time_needed = calculate_uninterrupted_time(sm, "current_flight_arrival")

                # if the state machine doesn't have enough time then we need to delay the arrival 
                if uninterrupted_time_needed > gap:

                    # calculate how much time we need to delay the arrival time by to make the the airplane land on time assuming no more delays
                    delay_amount = uninterrupted_time_needed - gap

                    # delay the arrival time and update the arrival status 
                    airplane["arrivalTime"] = float(arrival_time + delay_amount)
                    airplane["arrivalStatus"] = "Delayed" if airplane["arrivalStatus"] == "Scheduled" else airplane["arrivalStatus"] # if its on approach or something you want the status board to reflect that - not be overridden w/ delayed

            # if the airplane hasn't departed yet    
            if not (airplane.get("departureStatus") == "Departed"):

                # calculate how much time there is between now and when the plane is scheduled to depart
                departure_time = float(airplane["departureTime"])
                gap = departure_time - current_time

                # calculate how much time is needed for the state machine to get to the departed state
                uninterrupted_time_needed = calculate_uninterrupted_time(sm, "current_flight_departure")

                # if the state machine doesn't have enough time then we need to delay the departure 
                if uninterrupted_time_needed > gap:
                    # calculate how much time we need to delay the departure time by to make the the airplane land on time assuming no more delays
                    delay_amount = uninterrupted_time_needed - gap

                    # delay the departure time and update the departure status
                    airplane["departureTime"] = float(departure_time + delay_amount)
                    airplane["departureStatus"] = "Delayed" if airplane["departureStatus"] == "Scheduled" else airplane["departureStatus"] # if its boarding or something you want the status board to reflect that - not be overridden w/ delayed

            # assemble the update and add it to the list of updates
            batch_update.append({
                "sourceAirport": flight_name,
                "update": {
                    "arrivalTime": airplane["arrivalTime"],
                    "departureTime": airplane["departureTime"],
                    "arrivalStatus": airplane["arrivalStatus"],
                    "departureStatus": airplane["departureStatus"]
                }
            })

            # go to next flight
            previous_flight_arrival_time = airplane["arrivalTime"]
            continue

        # for the subsequent flights

        # calculate how much time there is between now and when the plane is scheduled to arrive
        arrival_time = float(airplane["arrivalTime"])
        # calculate gap between previous flight's updated arrival time (current time for second flight since first flight is still in progress) and current flight's arrival time
        gap = arrival_time - (previous_flight_arrival_time if i > (sm.current_flight_index + 1) else current_time)

        if previous_flight_arrival_time >= arrival_time:
            delay_amount = next_flight_arrival_uninterrupted_time_needed + delay_offset
            # delay the arrival and departure time and update the arrival and departure status
            airplane["arrivalTime"] = arrival_time + delay_amount
            airplane["departureTime"] = airplane["departureTime"] + delay_amount

            # assemble the update and add it to the list of updates
            batch_update.append({
                "sourceAirport": flight_name,
                "update": {
                    "arrivalTime": airplane["arrivalTime"],
                    "departureTime": airplane["departureTime"],
                    "arrivalStatus": "Delayed",
                    "departureStatus": "Delayed"
                }
            })

        # time needed greater than the gap
        elif next_flight_arrival_uninterrupted_time_needed > gap:
            print("next flight arrival uninterrupted time needed:", next_flight_arrival_uninterrupted_time_needed)
            print("gap:", gap)
            # calculate how much time we need to delay the departure time by to make the the airplane land on time assuming no more delays
            delay_amount = (next_flight_arrival_uninterrupted_time_needed - gap) + delay_offset

            # delay the arrival and departure time and update the arrival and departure status
            airplane["arrivalTime"] = (arrival_time + delay_amount)
            airplane["departureTime"] = (float(airplane["departureTime"]) + delay_amount)

            # assemble the update and add it to the list of updates
            batch_update.append({
                "sourceAirport": flight_name,
                "update": {
                    "arrivalTime": airplane["arrivalTime"],
                    "departureTime": airplane["departureTime"],
                    "arrivalStatus": "Delayed",
                    "departureStatus": "Delayed"
                }
            })
        
        # If no delay needed for this flight, none are needed for the rest
        else:
            break

        # Subsequent flights only need to maintain minimum spacing
        next_flight_arrival_uninterrupted_time_needed = config.minutes_per_airplane_cycle
        # previous flight arrival
        previous_flight_arrival_time = airplane["arrivalTime"]
        # increasing delay offset if it will stay within the delay cap
        delay_offset = min(delay_offset + config.delay_increment_per_flight, config.delay_offset_cap)

    # Send delay updates
    if batch_update:
        requests.patch(f'{config.airplanes_api_url}batch', json=batch_update, headers=config.api_headers)


def check_for_cancellation( sm , current_state):

    # hasn't arrived yet
    if current_state in ["state_three", "state_four", "state_five", "state_six", "state_twenty_five", "state_twenty_six", "state_twenty_seven", "state_twenty_eight"]:
        original_eta = float(sm.current_flight_object["arrivalTime"])
        max_eta = original_eta + config.max_arrival_delay
        projected_eta = sm.simulation_minutes + calculate_uninterrupted_time( sm, "current_flight_arrival" )

        return projected_eta > max_eta

    # arrived but not departed
    else:
        original_etd = float(sm.current_flight_object["departureTime"])
        max_etd = original_etd + config.max_departure_delay
        projected_etd = sm.simulation_minutes + calculate_uninterrupted_time( sm, "current_flight_departure" )

        return projected_etd > max_etd