from screeninfo import get_monitors
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# original code based on 3840 x 2160 screen resolution
screen_width_conversion_factor = screen_width / 3840
screen_height_conversion_factor = screen_height / 2160

state_machine_seconds_per_loop = 1.1

# airplane color
airplane_day_color = "red"
airplane_night_color = "green"
# flight_num color
flight_num_day_color = "Black"
flight_num_off_color = "Yellow"

# lights colors
approach_light_color = "lightgreen"
fuel_depot_light_color = "lightgreen"
left_beacon_light_color = "lightgreen"
right_beacon_light_color = "antiquewhite"
runway_light_color = "white"
taxiway_light_color = "violet"
VASI_color = "red"

gate_closed_color = "grey20"
gate_open_color = "red"