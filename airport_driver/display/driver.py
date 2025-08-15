# Maxwell Voeltner
# Airport Simulation

import pygame, math, time, json, data, config
from filelock import FileLock

# file lock for avoiding concurrency issues with that output
file_path = "../statemachine/output.txt"
lock = FileLock(f"{file_path}.lock")

# rotates airplane around its pivot by radian degrees clockwise
def rotate_airplane(radians, position):
    
    # getting x and y coordinates of pivot of airplane
    pivot_x, pivot_y = position

    #changing every coordinate in airplane to rotated coordinate
    for i in range(len(airplane)):

        # getting x and y coordinates of current index
        x, y = airplane[i]

        # calculating rotated x and y coords
        # 1) calculate coords relative to pivot (translate coords to be pivoted about the origin)
        # 2) rotate coords about the origin
        # 3) translate coords back
        rotated_x = pivot_x + (x - pivot_x) * math.cos(radians) - (y - pivot_y) * math.sin(radians)
        rotated_y = pivot_y + (y - pivot_y) * math.cos(radians) + (x - pivot_x) * math.sin(radians)

        # update airplane coords to rotated coordinates (rounded because the calclations result in irrationals ex (.999999))
        airplane[i] = (round(rotated_x), round(rotated_y))


# translates the airplane to new position
def update_airplane_position(new_position, position):
    
    # getting x and y coordinates of new pivot (position)
    new_position_x, new_position_y = new_position
    # getting x and y coordinaes of current pivot (position)
    x, y = position

    # calculating change in x and change in y coordinates for translation
    delta_x = new_position_x - x
    delta_y = new_position_y - y

    # changing every coordinate in airplane to translated coordinate
    for i in range(len(airplane)):

        # getting x and y coordinates of current index
        x, y = airplane[i]

        # translating the coordinates
        x += delta_x
        y += delta_y

        # update airplane coords to rotated coordinates (rounded because some calculations are irrational)
        airplane[i] = (x, y)

    # updating position of flight number text box
    flight_num_text_box.left += delta_x
    flight_num_text_box.top += delta_y


def airplane_animation(start_pos, end_pos, start_radians, end_radians, elapsed_time, duration):
    t = elapsed_time / duration
    x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
    y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
    delta = (end_radians - start_radians + math.pi) % (2 * math.pi) - math.pi
    radians = start_radians + delta * t
    return ((x, y), radians)

def airplane_holding_pattern_animation(mode, elapsed_time, orbit_time=6):
    x, y = data.locs["25-origin"]
    t = (elapsed_time / orbit_time) % 1
    radians = (-2 * math.pi) * t
    x = x + ((300 * config.screen_width_conversion_factor) * math.cos(radians))
    y = y + ((300 * config.screen_width_conversion_factor) * math.sin(radians))
    return ((x, y), radians)


# gets flight num string
def get_flight_num_text(flight_num_string, day_bool):
    flight_num_color = config.flight_num_day_color if day_bool else config.flight_num_off_color
    return font.render(flight_num_string, True, flight_num_color)


# default airport inputs
vital_statuses = {
    "RW6L": False,
    "RW6R": False,
    "approach": False,
    "VASI": False,
    "taxiway": False,
    "fuel_depot": False,
    "beacon": False,
    "gate_open": False,
}

# pygame loop trackers
last_time = time.time()
airplane_transition_animation = False
previous_loc_num = 0
airplane_transition_animation_previous_position = data.locs["0"]
airplane_transition_animation_previous_radians = data.loc_radians["0"]
airplane_transition_animation_time = 0
holding_pattern_animation_time = 0
holding_pattern_last_position = data.locs["25"]
holding_pattern_last_radians = data.loc_radians["25"]
approach_anim_time = 0
beacon_anim_time = 0
gate_anim_time = 0
gate_close_anim_time = 0
previous_gate_open = False
gate_closing_sequence = False
previous_day = -1
day_to_night_transition = False
day_to_night_transition_time = 0
night_to_day_transition = False
night_to_day_transition_time = 0

# the simulation
pygame.init()
#pygame.mixer.init()

# setting the screen dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Load backgrounds to save time
background_day = pygame.image.load('day.png')
background_day = pygame.transform.scale(background_day, (config.screen_width, config.screen_height)).convert()
background_night = pygame.image.load('night.png')
background_night = pygame.transform.scale(background_night, (config.screen_width, config.screen_height)).convert()

# Load day - night maps
darkness_10_percent = pygame.transform.scale(pygame.image.load('10_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_20_percent = pygame.transform.scale(pygame.image.load('20_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_30_percent = pygame.transform.scale(pygame.image.load('30_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_40_percent = pygame.transform.scale(pygame.image.load('40_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_50_percent = pygame.transform.scale(pygame.image.load('50_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_60_percent = pygame.transform.scale(pygame.image.load('60_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_70_percent = pygame.transform.scale(pygame.image.load('70_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_80_percent = pygame.transform.scale(pygame.image.load('80_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_85_percent = pygame.transform.scale(pygame.image.load('85_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_90_percent = pygame.transform.scale(pygame.image.load('90_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_93_percent = pygame.transform.scale(pygame.image.load('93_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_95_percent = pygame.transform.scale(pygame.image.load('95_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_96_percent = pygame.transform.scale(pygame.image.load('96_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_97_percent = pygame.transform.scale(pygame.image.load('97_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_98_percent = pygame.transform.scale(pygame.image.load('98_-darkness.png'), (config.screen_width, config.screen_height)).convert()
darkness_99_percent = pygame.transform.scale(pygame.image.load('99_-darkness.png'), (config.screen_width, config.screen_height)).convert()

time_to_background = {
    0: background_day, 1: darkness_10_percent, 2: darkness_20_percent, 3: darkness_30_percent, 4: darkness_40_percent, 5: darkness_50_percent,
    6: darkness_60_percent, 7: darkness_70_percent, 8: darkness_80_percent, 9: darkness_90_percent, 10: darkness_93_percent, 11: darkness_95_percent,
    12: darkness_96_percent, 13: darkness_97_percent, 14: darkness_98_percent, 15: darkness_99_percent, 16: background_night
}

# Load font object to save time
font = pygame.font.Font("freesansbold.ttf", int(40 * config.screen_width_conversion_factor))

running = True

#the game loop
while running:
    a = time.time()
    #game stops when the 'x' button is hit on the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = time.time()
    delta_time = now - last_time
    last_time = now

    airplane_shape = data.airplane_shape
    airplane_shape_position = data.airplane_shape_position
    airplane = airplane_shape.copy() # assigning airplane the default location and size
    airplane_position = airplane_shape_position # assigning airplane pivot to the pivot of the default airplane
    airplane_rotation = 0 # assigning airplane rotation to 0 (defaut)

    # Reading from the file
    with lock:
        with open(file_path, "r") as file:
            input = json.loads(file.read())

    # storing input
    state_num = input["state"]
    loc_num = str(input["loc"])
    flight_num_string = input["flight_id"]
    mode = input["mode"]
    vital_statuses = {}
    vital_statuses["RW6L"] = input["RW6L"]
    vital_statuses["RW6R"] = input["RW6R"]
    vital_statuses["approach"] = input["approach"]
    vital_statuses["VASI"] = input["approach"]   # VASI in approach
    vital_statuses["taxiway"] = input["taxiway"]
    vital_statuses["fuel_depot"] = input["fuel_depot"]
    vital_statuses["beacon"] = input["beacon"]
    vital_statuses["gate_open"] = input["gate_open"]
    day = bool(input["day"])

    # getting state information
    new_position = data.locs[loc_num]
    airplane_rotation = data.loc_radians[loc_num]

    # you have to reset the entire screen to get rid of stuff - so everything has to be redrawn
    # start screen reset
    screen.fill("white") # ~ .005 seconds
    # set background to day or night based on day input
    if (previous_day == True and day == False): day_to_night_transition = True
    elif (previous_day == False and day == True): night_to_day_transition = True
    if day_to_night_transition:
        day_to_night_transition_time = min(16, day_to_night_transition_time + delta_time)
        background = time_to_background[int(day_to_night_transition_time)]
        if day_to_night_transition_time == 16: day_to_night_transition = False
        night_to_day_transition = False
        night_to_day_transition_time = 0
    elif night_to_day_transition:
        night_to_day_transition_time = min(16, night_to_day_transition_time + delta_time)
        background = time_to_background[int(16 - night_to_day_transition_time)]
        if night_to_day_transition_time == 16: night_to_day_transition = False
        day_to_night_transition = False
        day_to_night_transition_time = 0
    else: # just regular day or night
        background = background_day if day else background_night
        day_to_night_transition = False
        day_to_night_transition_time = 0
        night_to_day_transition = False
        night_to_day_transition_time = 0

    # adding background to screen
    screen.blit(background, (0, 0)) # ~ .008 seconds
    #end screen reset
    
    # drawing lights if their associated boolean is true
    # RW6L
    if (vital_statuses["RW6L"]):
        for coord in data.RW6L_positions:
            pygame.draw.circle(screen, config.runway_light_color, coord, 12 * config.screen_width_conversion_factor)

    # RW6R
    if (vital_statuses["RW6R"]):
        for coord in data.RW6R_positions:
            pygame.draw.circle(screen, config.runway_light_color, coord, 12 * config.screen_width_conversion_factor)

    # Taxiway
    if (vital_statuses["taxiway"]):
        for coord in data.taxiway_positions:
            pygame.draw.circle(screen, config.taxiway_light_color, coord, 12 * config.screen_width_conversion_factor)

    # Vasi
    if (vital_statuses["VASI"]):
        for coord in data.VASI_positions:
            pygame.draw.circle(screen, config.VASI_color, coord, 24 * config.screen_width_conversion_factor)

    # approach
    approach_anim_time = (approach_anim_time + delta_time) % 1
    if (vital_statuses["approach"]):
        if (approach_anim_time < 0.25):
            for i in range(4):
                pygame.draw.circle(screen, config.approach_light_color, data.approach_positions[i+4], 6 * config.screen_width_conversion_factor)
        elif (approach_anim_time < 0.5):
            pygame.draw.circle(screen, config.approach_light_color, data.approach_positions[3], 6 * config.screen_width_conversion_factor)
        elif (approach_anim_time < 0.75):
            pygame.draw.circle(screen, config.approach_light_color, data.approach_positions[2], 6 * config.screen_width_conversion_factor)
        else:
            pygame.draw.circle(screen, config.approach_light_color, data.approach_positions[1], 6 * config.screen_width_conversion_factor)

    # beacon
    beacon_anim_time = (beacon_anim_time + delta_time) % 2
    if (vital_statuses["beacon"]):

        if (beacon_anim_time < 1):
            pygame.draw.circle(screen, config.left_beacon_light_color, data.beacon_positions[0], 30 * config.screen_width_conversion_factor)
        else:
            pygame.draw.circle(screen, config.right_beacon_light_color, data.beacon_positions[1], 30 * config.screen_width_conversion_factor)

    # fuel depot
    if (vital_statuses["fuel_depot"]):
        pygame.draw.circle(screen, config.fuel_depot_light_color, data.fuel_depot_light_position, 12 * config.screen_width_conversion_factor)

    # gate
    if (not vital_statuses["gate_open"]):
        gate_anim_time = 0
        gate_closing_sequence = True if previous_gate_open else gate_closing_sequence
        if gate_closing_sequence:
            gate_close_anim_time = min((gate_close_anim_time + delta_time), 4) # capped at 4 cause that's all the way closed
            pygame.draw.rect(screen, config.gate_open_color, (data.gate_x_pos, data.closed_gate_y_pos - ((4 - gate_close_anim_time) / 4) * data.gate_height, data.gate_width, data.gate_height))
            gate_closing_sequence = False if gate_close_anim_time == 4 else True
        else:
            pygame.draw.rect(screen, config.gate_closed_color, (data.gate_x_pos, data.closed_gate_y_pos, data.gate_width, data.gate_height))
    else:
        gate_close_anim_time = 0
        gate_closing_sequence = False
        gate_anim_time = min((gate_anim_time + delta_time), 4) # capped at 4 cause that's all the way open
        pygame.draw.rect(screen, config.gate_open_color, (data.gate_x_pos, data.closed_gate_y_pos - (gate_anim_time / 4) * data.gate_height, data.gate_width, data.gate_height))
    
    # drawing vital status
    period = "day" if day else "night"
    # flipping gate value for the status drawing (ex: gate_open == True --> gate==False because True is "good" and "False" is bad for the drawing)
    vital_statuses["gate"] = not vital_statuses["gate_open"]
    vitals = data.state_vital_components[state_num][period]
    pygame.draw.rect(screen, "grey40", (0, config.screen_height * (.84), config.screen_width * (.1), config.screen_height))

    text_surface = font.render("VITALS", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (config.screen_width * (.05), config.screen_height * (.86))
    screen.blit(text_surface, text_rect)

    # Start drawing vitals underneath the header
    line_spacing = font.get_linesize() + 12  # or adjust for your preferred spacing
    start_y = config.screen_height * (.9)   # tweak this for your display

    for i, vital in enumerate(vitals):
        # For display, you might want friendlier names:
        vital_label = vital.replace("_", " ").upper()  # Or use a lookup dict for labels
        vital_surface = font.render(vital_label, True, (255, 255, 255))
        vital_rect = vital_surface.get_rect()
        vital_rect.midleft = (config.screen_width * (.02), start_y + i * line_spacing)
        screen.blit(vital_surface, vital_rect)
        color = (0, 255, 0) if vital_statuses[vital] else (255, 0, 0)
        pygame.draw.circle(screen, color, (config.screen_width * (.01), start_y + i * line_spacing), config.screen_height * (.01))
    
    # Creating text object for flight number
    flight_num_text = get_flight_num_text(flight_num_string, day)
    # Creating text surface (get the rect of the text itself)
    flight_num_text_box = flight_num_text.get_rect()
    # Adjusting the width based on screen width conversion factor
    flight_num_text_box.width += 15 * config.screen_width_conversion_factor
    # Positioning the flight number text (above the airplane by default)
    flight_num_text_box.left = 50 * config.screen_width_conversion_factor
    flight_num_text_box.top = -45 * config.screen_width_conversion_factor
    
    # arranging the airplane

    # start the transition animation to current state
    if previous_loc_num != loc_num:
        airplane_transition_animation_previous_position = data.locs[str(previous_loc_num)] if (previous_loc_num != "25") else holding_pattern_last_position
        airplane_transition_animation_previous_radians = data.loc_radians[str(previous_loc_num)] if (previous_loc_num != "25") else holding_pattern_last_radians
        airplane_transition_animation = True

    # if we're in the middle of a transition animation
    if airplane_transition_animation:
        if previous_loc_num != loc_num: # state has already changed to the state after the one we're in the middle of getting to
            airplane_transition_animation_previous_position = data.locs[str(previous_loc_num)] if (previous_loc_num != "25") else holding_pattern_last_position
            airplane_transition_animation_previous_radians = data.loc_radians[str(previous_loc_num)] if (previous_loc_num != "25") else holding_pattern_last_radians
            airplane_transition_animation_time = 0

        airplane_transition_animation_time = min(airplane_transition_animation_time + delta_time, (data.state_minimum_loops[mode][loc_num] + .05))
        if (loc_num == "0" and (airplane_transition_animation_previous_position not in data.locs.values())): # if we're going holding (state 25) --> state zero then its flying away so make the plane fly off the screen in the direction its already going
            airplane_rotation = airplane_transition_animation_previous_radians
            x, y = airplane_transition_animation_previous_position
            new_position = ((x + math.cos(-1 * airplane_rotation) * 3500 * config.screen_width_conversion_factor), (y + math.sin(-1 * airplane_rotation) * 3500 * config.screen_width_conversion_factor))
        new_position, airplane_rotation = airplane_animation(airplane_transition_animation_previous_position, new_position, airplane_transition_animation_previous_radians, airplane_rotation, airplane_transition_animation_time, data.state_minimum_loops[mode][loc_num])
        airplane_transition_animation = False if airplane_transition_animation_time == (data.state_minimum_loops[mode][loc_num] + .05) else True
    else:
        airplane_transition_animation_time = 0
    
    if (loc_num == "25" and not airplane_transition_animation): # if we're in holding and not transitioning to it (we already got there)
        holding_pattern_animation_time = holding_pattern_animation_time + delta_time
        new_position, airplane_rotation = airplane_holding_pattern_animation(mode, holding_pattern_animation_time)
        holding_pattern_last_position = new_position
        holding_pattern_last_radians = airplane_rotation
    else:
        holding_pattern_animation_time = 0
        holding_pattern_last_position = data.locs["25"]
        holding_pattern_last_radians = data.loc_radians["25"]

    rotate_airplane(airplane_rotation, airplane_position)
    
    # changing airplane position
    update_airplane_position(new_position, airplane_position)

    # drawing the airplane using color according to day/night situation
    if (day):
        pygame.draw.polygon(screen, config.airplane_day_color, airplane)
    else:
        pygame.draw.polygon(screen, config.airplane_night_color, airplane)

    # displaying the flight number
    screen.blit(flight_num_text, flight_num_text_box)

    # if the simulation ended
    if (state_num == "END"):
        # Create a surface for the background (gray rectangle)
        pygame.draw.rect(screen, "grey40", (config.screen_width * (.25), config.screen_height * (.25), config.screen_width * (.5), config.screen_height * (.5)))
        text_surface = font.render("SIMULATION OVER", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (config.screen_width // 2, config.screen_height // 2)
        screen.blit(text_surface, text_rect)

    # updating the screen
    pygame.display.update()

    previous_gate_open = vital_statuses["gate_open"]
    previous_loc_num = loc_num
    previous_day = day
    #print("frame time:", time.time() - a)

pygame.quit()