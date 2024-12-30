# Maxwell Voeltner
# Airport Simulation

import pygame, math, time, data
from filelock import FileLock

#rotates airplane around its pivot by radian degrees clockwise
def rotate_airplane(radians, position):
    
    #getting x and y coordinates of pivot of airplane
    pivot_x, pivot_y = position

    #changing every coordinate in airplane to rotated coordinate
    for i in range(len(airplane)):

        #getting x and y coordinates of current index
        x, y = airplane[i]

        #calculating rotated x and y coords
        # 1) calculate coords relative to pivot (translate coords to be pivoted about the origin)
        # 2) rotate coords about the origin
        # 3) translate coords back
        rotated_x = pivot_x + (x - pivot_x) * math.cos(radians) - (y - pivot_y) * math.sin(radians)
        rotated_y = pivot_y + (y - pivot_y) * math.cos(radians) + (x - pivot_x) * math.sin(radians)

        #update airplane coords to rotated coordinates (rounded because the calclations result in irrationals ex (.999999))
        airplane[i] = (round(rotated_x), round(rotated_y))


#translates the airplane to new position
def update_airplane_position(new_position, position):
    
    #getting x and y coordinates of new pivot (position)
    new_position_x, new_position_y = new_position
    #getting x and y coordinaes of current pivot (position)
    x, y = position

    #calculating change in x and change in y coordinates for translation
    delta_x = new_position_x - x
    delta_y = new_position_y - y

    #changing every coordinate in airplane to translated coordinate
    for i in range(len(airplane)):

        #getting x and y coordinates of current index
        x, y = airplane[i]

        #translating the coordinates
        x += delta_x
        y += delta_y

        #update airplane coords to rotated coordinates (rounded because some calculations are irrational)
        airplane[i] = (x, y)

    #updating position of flight number text box
    flight_num_text_box.left += delta_x
    flight_num_text_box.top += delta_y


#plays voice file
def play_voice_file(voice_file):

    pygame.mixer.music.load(voice_file)
    pygame.mixer.music.play()


#airport function default variables
previous_state = -1
beacon_counter = 0

#the simulation

pygame.init()

pygame.mixer.init()

#setting the screen dimensions
screen = pygame.display.set_mode((960, 540))

running = True

#the game loop
while running:

    #game stops when the 'x' button is hit on the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #default plane shape (static data - but the plane needs to be reset every iteration)
    airplane_shape = [(21, 4), (23, 4), (24, 5), (25, 7), (25, 14), (27, 16), (32, 18), (35, 20),
                (37, 22), (37, 24), (34, 23), (25, 20), (25, 27), (27, 29), (29, 30), (29, 31), (28, 32),
                (27, 31), (24, 31), (23, 33), (22, 34), (21, 33), (20, 31), (17, 31), (16, 32), (15, 31), (15, 30),
                (17, 29), (19, 27), (19, 20), (10, 23), (7, 24), (7, 22), (9, 20), (12, 18),
                (17, 16), (19, 14), (19, 7), (20, 5)]


    #default airplane position (static data - but the airplane position needs to be reset every iteration)
    airplane_shape_position = (22, 18)

    #assigning airplane the default location and size
    airplane = airplane_shape
    #assigning airplane pivot to the pivot of the default airplane
    airplane_position = airplane_shape_position
    #assigning airplane rotation to 0 (defaut)
    airplane_rotation = 0

    # File paths and lock
    file_path = "../statemachine/output.txt"
    lock = FileLock(f"{file_path}.lock")

    # Reading from the file
    with lock:
        with open(file_path, "r") as file:
            input = file.read().split(",")

    #storing input
    
    if (input[0] == "END"): # simulation ends denoted by END flag in position 0 of input
        end_flag, day, simulation_time, time_alcms_hacked, time_perimeter_breached, voice_jamming, calibration_okay = input

        screen.fill("white")
        #default the background image to daytime
        background = pygame.image.load('honoluluday.png')
        #if day_bool is false then it is night so set background to night
        if (day == "0"):
            background = pygame.image.load('honolulunight.png')
        #resizing background to fit screen
        background = pygame.transform.scale(background, (960, 540))
        #adding background to screen
        screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 30)
        large_font = pygame.font.Font(None, 50)  # Larger font for the "Red/Blue Team Wins!" text

        # Adjust the height of the box to make it a bit taller
        box_width, box_height = 400, 235  # Increased height
        box_x = (960 - box_width) // 2
        box_y = (540 - box_height) // 2  # Center the box vertically on the screen

        # Draw the grey rectangle for the box (background of the box)
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (169, 169, 169), box_rect)  # Fill with grey background

        # Draw the black border for the box
        pygame.draw.rect(screen, (0, 0, 0), box_rect, 5)  # Black border with thickness of 5

        # Prepare the text to display
        info_text = [
            f"Simulation Time: {simulation_time}",
            f"Time ALCMS Hacked: {time_alcms_hacked}",
            f"Time Perimeter Breached: {time_perimeter_breached}",
            f"Voice Jamming: {'Yes' if voice_jamming == '1' else 'No'}",
            f"Calibration Hacked: {'Yes' if calibration_okay == '1' else 'No'}"
        ]

        # Determine the winner based on voice_jamming and calibration_okay
        red_team_text = f"{'Blue' if voice_jamming == '1' and calibration_okay == '0' else 'Red'} Team Wins!"
        rendered_red_team = large_font.render(red_team_text, True, (0, 0, 0))  # Black color
        red_team_width = rendered_red_team.get_width()

        # Calculate position for the "Red/Blue Team Wins!" text inside the box
        red_team_x = (960 - red_team_width) // 2  # Center the text horizontally inside the box
        red_team_y = box_y + 20  # Position it slightly below the top of the box

        # Render and display the "Red/Blue Team Wins!" text inside the box
        screen.blit(rendered_red_team, (red_team_x, red_team_y))

        # Render and display the other info text inside the box
        y_offset = red_team_y + 50  # Starting y-position for the other text (below the "Red/Blue Team Wins!" text)
        for text in info_text:
            before_colon, after_colon = text.split(":", 1)  # Split the text into two parts: before and after the colon
            rendered_before = font.render(before_colon + ": ", True, (0, 0, 0))  # Render the part before the colon (black)
            screen.blit(rendered_before, (box_x + 30, y_offset))

            rendered_after = font.render(after_colon.strip(), True, (255, 0, 0))  # Render the part after the colon (red)
            screen.blit(rendered_after, (box_x + 30 + rendered_before.get_width(), y_offset))

            y_offset += 30  # Increase y-position for next line

        # Update the display
        pygame.display.update()

        continue # avoiding drawing any of the airport stuff

    # simulation is still running
    state_num, loc_num, alcms, day_bool, voice_file_num, flight_num_string = input
    alcms = int(alcms)
    loc_num = int(loc_num)
    day_bool = int(day_bool)

    #getting state information
    new_position = data.locs[loc_num]
    airplane_rotation = data.loc_radians[loc_num]
    voice_file = data.voice_files[voice_file_num]


    #you have to reset the entire screen to get rid of stuff so everything has to be redrawn

    #start screen reset

    screen.fill("white")
    #default the background image to daytime
    background = pygame.image.load('honoluluday.png')
    #if day_bool is false then it is night so set background to night
    if (not day_bool):
        background = pygame.image.load('honolulunight.png')
    #resizing background to fit screen
    background = pygame.transform.scale(background, (960, 540))
    #adding background to screen
    screen.blit(background, (0, 0))

    #end screen reset

    # drawing lights if their associated boolean is true
    if (alcms == 1):

        for coord in data.RW6L_positions:

            pygame.draw.circle(screen, "white", coord, 3)

        for coord in data.RW6R_positions:

            pygame.draw.circle(screen, "white", coord, 3)

        for coord in data.taxiway_positions:

            pygame.draw.circle(screen, "violet", coord, 3)

        for coord in data.RW6L_vasi_positions:

            pygame.draw.circle(screen, "Red", coord, 6)

        for coord in data.RW6L_apch_positions:

            pygame.draw.circle(screen, "White", coord, 3)

        for coord in data.beacon_gw_position:

            #cycling the beacon color
            if (beacon_counter < 40):
                pygame.draw.circle(screen, "green", coord, 10)
            else:
                pygame.draw.circle(screen, "white", coord, 10)

            if (beacon_counter == 80):
                beacon_counter = 0
            else:
                beacon_counter += 1

        for coord in data.ramp_positions:
            pygame.draw.circle(screen, "Violet", coord, 3)

        pygame.draw.circle(screen, "green", data.fuel_depot_light_position, 3)


    # creating text object for flight number
    font = pygame.font.Font("freesansbold.ttf", 10)
    # adding flight number to text object
    # chaning color of text based on day/night
    flight_num_color = data.flight_num_day_color
    if (not day_bool):
        flight_num_color = data.flight_num_off_color
    flight_num_text = font.render(flight_num_string, True, flight_num_color)
    # creating text surface
    flight_num_text_box = flight_num_text.get_rect()
    flight_num_text_box.width += 30
    # positioning the flight number above of the airplane (default positioned)
    flight_num_text_box.left = 10
    flight_num_text_box.top = -11

    
    # playing the voice file if the state changes (so the voice file only plays once at the start of a new state)
    if (state_num != previous_state):
        play_voice_file(voice_file)

    
    # arranging the airplane

    # rotate(clockwise) airplane by radians parameter
    rotate_airplane(airplane_rotation, airplane_position)
    
    # changing airplane position
    update_airplane_position(new_position, airplane_position)

    # drawing the airplane
    if (day_bool):
        pygame.draw.polygon(screen, "Red", airplane)
    else:
        pygame.draw.polygon(screen, "Green", airplane)

    # displaying the flight number
    screen.blit(flight_num_text, flight_num_text_box)

    #updating the screen
    pygame.display.update()

    #updating previous state to current state
    previous_state = state_num

pygame.quit()
