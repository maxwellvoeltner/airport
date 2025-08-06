import math, config

# Static data with scaled coordinates

airplane_shape = [
        (84, 16), (92, 16), (96, 20), (100, 28), (100, 56), (108, 64), (128, 72), (140, 80),
        (148, 88), (148, 96), (136, 92), (100, 80), (100, 108), (108, 116), (116, 120), (116, 124), 
        (112, 128), (108, 124), (96, 124), (92, 132), (88, 136), (84, 132), (80, 124), (68, 124), 
        (64, 128), (60, 124), (60, 120), (68, 116), (76, 108), (76, 80), (40, 92), (28, 96), 
        (28, 88), (36, 80), (48, 72), (68, 64), (76, 56), (76, 28), (80, 20)
    ]

airplane_shape = [
    (x * config.screen_width_conversion_factor, y * config.screen_height_conversion_factor)
    for x, y in airplane_shape
]

airplane_shape_position = (88 * config.screen_width_conversion_factor, 72 * config.screen_height_conversion_factor) # default airplane position (static data - but the airplane position needs to be reset every iteration)

# Location numbers mapped to on-screen position coordinates
locs = {
    '0': (-400, -400), '1': (200, 160), '2': (280, 620), 
    '3': (400, 1000), '4': (560, 1540), '5': (840, 2000), 
    '6': (1724, 2080), '7': (1916, 1760), '8': (1916, 1160), 
    '9': (1840, 620), '10': (1956, 440), '11': (2360, 440), 
    '12': (2700, 440), '13': (2780, 660),
    '14.1': (3040, 760), '14.2': (2940, 760), '14.3': (2840, 760),
    '14.4': (2840, 945), '14.5': (2940, 945), '14.6': (3040, 945),
    '15': (2760, 940), '16': (2720, 1280), '17': (2720, 1680), 
    '18': (2720, 1920), '19': (2360, 1920), '20': (2348, 1740), 
    '21': (2348, 1360), '22': (2348, 660), '23': (2348, 140), 
    '24': (2360, -400), '25': (160, 640), '26': (160, 320), 
    '27': (480, 320), '28': (480, 640)
}

# location coordinates adjusted for screen resolution
locs = {
    key: (
        x * config.screen_width_conversion_factor, 
        y * config.screen_height_conversion_factor
    )
    for key, (x, y) in locs.items()
}

# Degrees in radians of airplane in each location
loc_radians = {
    '0': 0, '1': (11 * math.pi / 12), '2': (11 * math.pi / 12), '3': (7 * math.pi / 8), '4': (5 * math.pi / 6),
    '5': (3 * math.pi / 5), '6': (math.pi / 4), '7': 0, '8': 0, '9': 0, '10': (2 * math.pi) / 5,
    '11': math.pi / 2, '12': (3 * math.pi / 4), '13': (9 * math.pi / 10), '14.1': math.pi,
    '14.2': math.pi, '14.3': math.pi, '14.4': 0, '14.5': 0, '14.6': 0, '15': (5 * math.pi) / 4,
    '16': math.pi, '17': math.pi, '18': (5 * math.pi / 4), '19': (7 * math.pi / 4), '20': 0,
    '21': 0, '22': 0, '23': 0, '24': 0, '25': (7 * math.pi / 4),
    '26': math.pi / 4, '27': (3 * math.pi / 4), '28': (5 * math.pi / 4)
}

# Voice file number mapped to name of mp3 file
voice_files = {
    '0.0': "airplane-landing-6732.mp3", '1.0': "1.0.wav", '2.0': "2.0.wav",
    '3.0': "3.0.wav", '4.0': "4.0.wav", '5.0': "5.0.wav", '6.0': "6.0.wav", '7.0': "7.0.wav", 
    '8.0': "8.0.wav", '9.0': "9.0.wav", '10.0': "10.0.wav", '11.0': "11.0.wav", '12.0': "12.0.wav", 
    '13.0': "13.0.wav", '14.0': "14.0.wav", '15.0': "15.0.wav", '16.0': "16.0.wav", '17.0': "17.0.wav", 
    '18.0': "18.0.wav", '20.0': "20.0.wav", '21.0': "21.0.wav", '22.0': "22.0.wav", '23.0': "23.0.wav", 
    '24.0': "24.0.wav", '25.0': "25.0.wav", '26.0': "26.0.wav"
}

# List only the vitals you care about for your display
vital_names = [
    "day", "RW6L", "RW6R", "approach", "VASI",
    "taxiway", "fuel_depot", "beacon", "gate"
]

# Vitals lists
day_vitals = ["gate"]
can_land_night_vitals = ["beacon", "approach", "RW6L", "gate"]
can_advance_RW6L_vitals = ["day", "RW6L", "gate"]
can_fuel_vitals = ["RW6L", "fuel_depot", "gate"]
can_advance_taxiway_vitals = ["taxiway", "gate"]
can_advance_ramp_vitals = ["gate"]
can_advance_RW6R_vitals = ["RW6R", "gate"]

# State-to-vitals mapping using state names as keys
state_vital_components = {
    "state_zero":        {"day": [], "night": []},
    "state_one":         {"day": [], "night": []},
    "state_two":         {"day": [], "night": []},
    "state_three":       {"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_four":        {"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_five":        {"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_six":         {"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_seven":       {"day": ["gate"], "night": ["RW6L", "gate"]},
    "state_eight":       {"day": ["gate"], "night": ["RW6L", "gate"]},
    "state_nine":        {"day": ["fuel_depot", "gate"], "night": ["RW6L", "fuel_depot", "gate"]},
    "state_ten":         {"day": ["gate"], "night": ["taxiway", "gate"]},
    "state_eleven":      {"day": ["gate"], "night": ["taxiway", "gate"]},
    "state_twelve":      {"day": ["gate"], "night": ["gate"]},
    "state_thirteen":    {"day": ["gate"], "night": ["gate"]},
    "state_fourteen":    {"day": ["gate"], "night": ["gate"]},
    "state_fifteen":     {"day": ["gate"], "night": ["gate"]},
    "state_sixteen":     {"day": ["gate"], "night": ["taxiway", "gate"]},
    "state_seventeen":   {"day": ["gate"], "night": ["taxiway", "gate"]},
    "state_eighteen":    {"day": ["gate"], "night": ["taxiway", "gate"]},
    "state_nineteen":    {"day": ["gate"], "night": ["taxiway", "gate"]},
    "state_twenty":      {"day": ["gate"], "night": ["RW6R", "gate"]},
    "state_twenty_one":  {"day": ["gate"], "night": ["RW6R", "gate"]},
    "state_twenty_two":  {"day": ["gate"], "night": ["RW6R", "gate"]},
    "state_twenty_three":{"day": [], "night": []},
    "state_twenty_four": {"day": [], "night": []},
    "state_twenty_five": {"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_twenty_six":  {"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_twenty_seven":{"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
    "state_twenty_eight":{"day": ["gate"], "night": ["beacon", "approach", "RW6L", "gate"]},
}

# Left Runway Lights coordinates
RW6L_positions = [
    (1832, 1680), (1832, 1600), (1832, 1520), (1832, 1440), 
    (1832, 1360), (1832, 1280), (1832, 1200), (1832, 1120), 
    (1832, 1040), (1832, 960), (1832, 880), (1832, 800), 
    (1832, 720), (1832, 640), (1832, 560), (1997, 1680), 
    (1997, 1600), (1997, 1520), (1997, 1440), (1997, 1360), 
    (1997, 1280), (1997, 1200), (1997, 1120), (1997, 1040), 
    (1997, 960), (1997, 880), (1997, 800), (1997, 720), 
    (1997, 640), (1997, 560)
]

# Left Runway Lights coordinates adjusted for screen resolution
RW6L_positions = [
    (x * config.screen_width_conversion_factor, y * config.screen_height_conversion_factor)
    for x, y in RW6L_positions
]

# RW6R (RW6L translated to the right runway)
RW6R_positions = []
for coord in RW6L_positions:
    x, y = coord
    x += 436 * config.screen_width_conversion_factor
    RW6R_positions.append((x, y))

# Taxiway
taxiway_positions = [
    (2056, 376), (2136, 376), (2216, 376), (2056, 496), 
    (2136, 496), (2216, 496), (2488, 376), (2568, 376),
    (2648, 376), (2488, 496), (2568, 496), (2648, 496),

    (2856, 1088), (2856, 1188), (2856, 1288), (2856, 1388),
    (2856, 1488), (2856, 1588), (2856, 1688), (2856, 1788),
    (2856, 1888), (2856, 1988),

    (2554, 588), (2554, 688), (2554, 788), (2554, 888), (2554, 988),
    (2554, 1088), (2554, 1188), (2554, 1288), (2554, 1388),
    (2554, 1488), (2554, 1588), (2554, 1688), (2544, 1776), (2476, 1820),
    
    (2776, 2060), (2676, 2060),
    (2576, 2060), (2476, 2060), (2376, 2060), (2276, 2060)
]

# Taxiway lights adjusted for screen resolution
taxiway_positions = [
    (x * config.screen_width_conversion_factor, y * config.screen_height_conversion_factor)
    for x, y in taxiway_positions
]

# VASI
VASI_positions = [(1800, 1760), (2034, 1760)]

# VASI adjusted for screen resolution
VASI_positions = [
    (x * config.screen_width_conversion_factor, y * config.screen_height_conversion_factor)
    for x, y in VASI_positions
]

# Approach lights
approach_positions = [(1916, 1940), (1916, 1970), (1916, 2000), (1916, 2030),
                       (1886, 2050), (1906, 2050), (1926, 2050), (1946, 2050)]

# Approach lights adjusted for screen resolution
approach_positions = [
    (x * config.screen_width_conversion_factor, y * config.screen_height_conversion_factor)
    for x, y in approach_positions
]

# Fuel depot light
fuel_depot_light_position = (1780 * config.screen_width_conversion_factor, 690 * config.screen_height_conversion_factor)

# Beacon GW
beacon_positions = [(1660, 1940), (1680, 1940)]

# Beacon adjusted for screen resolution
beacon_positions = [
    (x * config.screen_width_conversion_factor, y * config.screen_height_conversion_factor)
    for x, y in beacon_positions
]

# gate
gate_x_pos = 1517 * config.screen_width_conversion_factor
closed_gate_y_pos = 480 * config.screen_height_conversion_factor
gate_width = 15 * config.screen_width_conversion_factor
gate_height = 90 * config.screen_height_conversion_factor