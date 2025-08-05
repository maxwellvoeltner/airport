import config

# timing
def minutes_to_time(minutes):

    minutes = int(minutes)
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}:{remaining_minutes:02d}"

# dynamically calculates timing info for the driver
def calculate_timing(state_times):

    iteration_total = 0
    iterations_to_land = 0
    iterations_to_depart = 0
    s0_min = 0

    for state, num in state_times.items():
        if state == "s0_min":
            s0_min = num
        elif state == "s7_min":
            iterations_to_land = iteration_total
        elif state == "s23_min":
            iterations_to_depart = iteration_total
        elif state == "holding_min":
            continue
        iteration_total += num

    minutes_per_loop = config.minutes_per_airplane_cycle / iteration_total
    time_to_arrive = (iterations_to_land) * minutes_per_loop
    time_to_arrive_from_state_zero = time_to_arrive - (s0_min * minutes_per_loop)
    time_to_depart = iterations_to_depart * minutes_per_loop

    start_time = config.initial_airplanes[0].get("arrivalTime") - time_to_arrive
    if start_time < 0:
        start_time += 1440

    return {
        "iterations_in_uninterrupted_cycle": iteration_total,
        "minutes_per_loop": minutes_per_loop,
        "time_to_arrive_from_state_zero": time_to_arrive_from_state_zero,
        "time_to_arrive": time_to_arrive,
        "time_to_depart": time_to_depart,
        "start_time": start_time
    }


# prints the timing information for me to see
def print_startup_summary(mode, timing):
    print("====================================")
    print(f"Simulation Mode: {mode.upper()}")
    print(f"Start Time: {minutes_to_time(timing['start_time'])} ({timing['start_time']} min)")
    print(f"Minutes per Loop: {timing['minutes_per_loop']:.2f}")
    print(f"Iterations per Flight Cycle: {timing['iterations_in_uninterrupted_cycle']}")
    print(f"Time to arrive from state zero: {timing['time_to_arrive_from_state_zero']:.2f} min ({minutes_to_time(timing['time_to_arrive_from_state_zero'])})")
    print(f"Relative Arrival Time: {timing['time_to_arrive']:.2f} min ({minutes_to_time(timing['time_to_arrive'])})")
    print(f"Relative Departure Time: {timing['time_to_depart']:.2f} min ({minutes_to_time(timing['time_to_depart'])})")
    print("====================================")