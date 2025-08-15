import config
from fractions import Fraction

def validate_minutes_config():
    assert isinstance(config.minutes_per_airplane_cycle, int) and (0 < config.minutes_per_airplane_cycle < 240), \
        "minutes_per_airplane_cycle must be a positive integer"
    assert isinstance(config.competition_mode_maximum_time_in_minutes, int) and config.competition_mode_maximum_time_in_minutes > 0, \
        "competition_mode_maximum_time_in_minutes must be a positive integer"


def validate_delay_settings():
    assert isinstance(config.delay_increment_per_flight, int) and config.delay_increment_per_flight >= 0, \
        "delay_increment_per_flight must be a non-negative integer"
    assert isinstance(config.delay_checker_frequency, int) and config.delay_checker_frequency > 0, \
        "delay_increment_per_flight must be a non-negative integer"
    assert isinstance(config.delay_offset_cap, int) and config.delay_offset_cap >= 0, \
        "delay_offset_cap must be a non-negative integer"


def validate_airplane_schedule():
    airplanes = config.initial_airplanes
    source_airports = set()
    prev_arrival = -1
    cycle_time = config.minutes_per_airplane_cycle

    for i, flight in enumerate(airplanes):
        src = flight["sourceAirport"]
        assert src not in source_airports, f"{src} used multiple times - can only be used once"
        source_airports.add(src)

        arrival_time = flight["arrivalTime"]
        assert isinstance(arrival_time, int) and arrival_time >= 0, f"Invalid arrivalTime for {src}"

        if i > 0:  
            assert arrival_time - prev_arrival >= cycle_time, f"Flight from {src} is scheduled too close to previous flight"

        prev_arrival = arrival_time


def validate_state_minimum_loops():
    def is_terminating_decimal(x):
        frac = Fraction(x).limit_denominator()
        denominator = frac.denominator
        while denominator % 2 == 0:
            denominator //= 2
        while denominator % 5 == 0:
            denominator //= 5
        return denominator == 1

    cycle_time = config.minutes_per_airplane_cycle

    for mode, state_dict in config.state_minimum_loops.items():
        total_loops = sum(v for k, v in state_dict.items() if k != "holding_min")
        assert total_loops > 0, f"Total loops in mode '{mode}' must be positive"
        minutes_per_loop = cycle_time / total_loops
        assert is_terminating_decimal(minutes_per_loop), \
            f"minutes_per_airplane_cycle / total_loops ({config.minutes_per_airplane_cycle} / {total_loops}) must be a terminating decimal in {mode} mode"


def validate_api_headers():
    headers = config.api_headers
    assert isinstance(headers, dict), "api_headers must be a dictionary"
    assert headers.get("Content-Type") == "application/json", "Content-Type must be application/json"
    assert isinstance(headers.get("x-auth-token"), str), "Missing or invalid x-auth-token"


def run_all_validations():
    validate_minutes_config()
    validate_delay_settings()
    validate_airplane_schedule()
    validate_state_minimum_loops()
    validate_api_headers()
    print("Config validation passed.")