# how many minutes it takes for the airplane to complete a normal path through the airport ( flying in -> ... -> flying away )
minutes_per_airplane_cycle = 120

# how many real life minutes COMPETITION mode runs for
competition_mode_maximum_time_in_minutes = 30

# amount each subsequent flight is delayed more than the previously delayed flight
'''
example of what this means:
    - flight 1 is stuck at the gate
    - flight 2 is delayed because of flight 1
    - flight 3 also needs to be delayed because the new delayed window for flight 2 pushes into the window for flight 3
    - flight 3 is delayed 10 minutes more than flight 2 was delayed
    - this prevents each flight from being delayed everytime a new delay occurs
    - you give the flights further back ( like flight 3 ) a safety buffer so hopefully you can leave it alone even if theres a bit more of a delay still to come with flight 1
'''
delay_increment_per_flight = 10

# maximum on how much more a flight can be delayed than the minimum amount necessary to keep the schedule on point
'''
prevents a situation like:
    - flight 1 created a 3 hour delay so now ALL ( lets say 9 ) subsequent flights are impacted
    - this prevents flight 9 from being delayed by a lot
    - without it there would create unnecessarily huge amounts of spacing ( more than a safety buffer ) between later flights
'''
delay_offset_cap = 30
max_arrival_delay = 30
max_departure_delay = 120
delay_checker_frequency = 10
'''
flights information
rules:
    - "sourceAirport" needs to be unique
    - "arrivalTime" must be in the range [0, 1440)
    - arrival times should be at least < minutes_per_airplane_cycle > apart ( otherwise you're gonna have to wait a long time to get to the next flight )
note:
    the departure times get automatically synced-up with the arrival times to fit the timing of the simulation based on the minutes_per_airplane_cycle
    so the "departureTime" values don't matter here
'''
initial_airplanes = [
    { "sourceAirport": "LAX", "arrivalFlight": "WN1500", "arrivalTime": 720, "arrivalStatus": "Scheduled", "departureFlight": "WN1501", "departureTime": 797, "departureStatus": "Scheduled", "gate": 1 },
    { "sourceAirport": "SFO", "arrivalFlight": "F9265", "arrivalTime": 855, "arrivalStatus": "Scheduled", "departureFlight": "F9266", "departureTime": 932, "departureStatus": "Scheduled", "gate": 2 },
    { "sourceAirport": "SEA", "arrivalFlight": "AA900", "arrivalTime": 990, "arrivalStatus": "Scheduled", "departureFlight": "AA901", "departureTime": 1067, "departureStatus": "Scheduled", "gate": 3 },
    { "sourceAirport": "PDX", "arrivalFlight": "UA2103", "arrivalTime": 1126, "arrivalStatus": "Scheduled", "departureFlight": "UA2104", "departureTime": 1203, "departureStatus": "Scheduled", "gate": 4 },
    { "sourceAirport": "SAN", "arrivalFlight": "DL1202", "arrivalTime": 1265, "arrivalStatus": "Scheduled", "departureFlight": "DL1203", "departureTime": 1342, "departureStatus": "Scheduled", "gate": 5 },
    { "sourceAirport": "LAS", "arrivalFlight": "NK740", "arrivalTime": 1405, "arrivalStatus": "Scheduled", "departureFlight": "NK741", "departureTime": 1482, "departureStatus": "Scheduled", "gate": 1 },
    { "sourceAirport": "PHX", "arrivalFlight": "B61720", "arrivalTime": 1550, "arrivalStatus": "Scheduled", "departureFlight": "B61721", "departureTime": 1627, "departureStatus": "Scheduled", "gate": 2 },
    { "sourceAirport": "DEN", "arrivalFlight": "WN505", "arrivalTime": 1695, "arrivalStatus": "Scheduled", "departureFlight": "WN506", "departureTime": 1772, "departureStatus": "Scheduled", "gate": 3 },
    { "sourceAirport": "DFW", "arrivalFlight": "AS1182", "arrivalTime": 1840, "arrivalStatus": "Scheduled", "departureFlight": "AS1183", "departureTime": 1917, "departureStatus": "Scheduled", "gate": 4 },
    { "sourceAirport": "ORD", "arrivalFlight": "WN3421", "arrivalTime": 1990, "arrivalStatus": "Scheduled", "departureFlight": "WN3422", "departureTime": 2067, "departureStatus": "Scheduled", "gate": 5 }
]

'''
the minimum number of loops ( ~ 1.1 seconds ) the airplane must stay in a state before being allowed to transition to the next state in the normal path
syntax: s#_min where # is the numerical representation of the state name
note:
    the total of the values in each mode are used to calculate minutes per loop
    that value needs to be a terminating decimal - otherwise we accumulate loss overtime
    so the sum all the loop numbers except holding divided by the minutes_per_airplane_cycle must be a terminating decimal

THIS NEEDS TO BE IN THE DISPLAY DRIVER data.py
'''
state_minimum_loops = {
    "demo": {
        "s0_min": 3,
        "s1_min": 3,
        "s2_min": 2,
        "s3_min": 2,
        "s4_min": 2,
        "s5_min": 2,
        "s6_min": 2,
        "s7_min": 2,
        "s8_min": 3,
        "s9_min": 7,
        "s10_min": 2,
        "s11_min": 2,
        "s12_min": 2,
        "s13_min": 2,
        "s14_min": 8,
        "s15_min": 2,
        "s16_min": 2,
        "s17_min": 2,
        "s18_min": 2,
        "s19_min": 2,
        "s20_min": 2,
        "s21_min": 1,
        "s22_min": 1,
        "s23_min": 1,
        "s24_min": 1,
        "holding_min": 2
    },

    # COMPETITION mode values can be customized to however long it feels appropraite to be in each state and should be at-least how long the voice files for that state are
    "competition": {
        "s0_min": 3,
        "s1_min": 3,
        "s2_min": 2,
        "s3_min": 2,
        "s4_min": 2,
        "s5_min": 2,
        "s6_min": 2,
        "s7_min": 2,
        "s8_min": 3,
        "s9_min": 7,
        "s10_min": 2,
        "s11_min": 2,
        "s12_min": 2,
        "s13_min": 2,
        "s14_min": 8,
        "s15_min": 2,
        "s16_min": 2,
        "s17_min": 2,
        "s18_min": 2,
        "s19_min": 2,
        "s20_min": 2,
        "s21_min": 1,
        "s22_min": 1,
        "s23_min": 1,
        "s24_min": 1,
        "holding_min": 2
    }
}

# backend base api url
airplanes_api_url = "http://localhost:2000/api/airplanes/"

# x-factor-authentication needed for the api request to work
api_headers = {
        'Content-Type': 'application/json',
        'x-auth-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik1heCIsInJvbGVzIjoiQWRtaW4iLCJpYXQiOjE3MTkzMzQ3Njl9.V7lqhmQZ996Vs3jNxLwjD01inR8aiuy8hpI-gm9IiFE'
    }

# the route to the simulationTime
simulation_time_url = "http://localhost:2000/simulationTime/"

# i/o ips
alcms_ip = "172.22.1.8"
fuel_ip = "172.29.1.5"
gate_ip = "172.24.1.11"
gate_arm = "O:0/0"

ALCMS_MARKERS = {
    "RW6L_on": (0, 1), # M: 0.1
    "RW6L_off": (0, 2), # M: 0.2
    "RW6R_on": (0, 4),
    "RW6R_off": (0, 5),
    "RW6R_output": (0, 6), # M: 0.5
    "taxiway_lights": (0, 3) # Q: 12.5
}

fuel_input_coil = 2