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


# plays voice file
def play_voice_file(voice_file, mode):
    pygame.mixer.music.load(voice_file)
    pygame.mixer.music.set_volume(0 if (mode == 'demo') else 1)
    pygame.mixer.music.play()

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
previous_state = -1
approach_anim_time = 0
beacon_anim_time = 0
gate_anim_time = 0
gate_close_anim_time = 0
previous_gate_open = False
gate_closing_sequence = False

# the simulation
pygame.init()
pygame.mixer.init()

#setting the screen dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Load backgrounds to save time
background_day = pygame.image.load('day.png')
background_day = pygame.transform.scale(background_day, (config.screen_width, config.screen_height)).convert()
background_night = pygame.image.load('night.png')
background_night = pygame.transform.scale(background_night, (config.screen_width, config.screen_height)).convert()

# Load font object to save time
font = pygame.font.Font("freesansbold.ttf", int(40 * config.screen_width_conversion_factor))

running = True

#the game loop
while running:
    
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
    voice_file_num = input["voice_file"]
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
    voice_file = data.voice_files[voice_file_num]

    # you have to reset the entire screen to get rid of stuff - so everything has to be redrawn
    # start screen reset
    screen.fill("white")
    # set background to day or night based on day input
    background = background_day if day else background_night
    #adding background to screen
    screen.blit(background, (0, 0))
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
    
    # playing the voice file if the state changes (so the voice file only plays once at the start of a new state)
    if (state_num != previous_state):
        play_voice_file(voice_file, mode)

    # arranging the airplane

    # rotate(clockwise) airplane by radians parameter
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
    previous_state = state_num # updating previous state to current state

pygame.quit()