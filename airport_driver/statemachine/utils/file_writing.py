import json
from filelock import FileLock

# file lock for concurrency issue avoidance since there's 2 files accessing that output file
file_path = "./output.txt"
lock = FileLock(f"{file_path}.lock")

# sends out airport and airplane information to a file for the display driver to read
def send_environment(sm, env):
    with lock:
        with open(file_path, "w") as file:
            # Build the dictionary
            output = {
                "state": sm.current_state.name,
                "loc": sm.loc,
                "RW6L": env["RW6L_lights"],
                "RW6R": env["RW6R_lights"],
                "approach": env["approach_lights"],
                "taxiway": env["taxiway_lights"],
                "fuel_depot": env["fuel_depot_light"],
                "beacon": env["beacon_light"],
                "gate_open": env["gate_open"],
                "day": sm.day,
                "voice_file": sm.voiceComm,
                "flight_id": sm.current_flight_id,
                "mode": sm.mode
            }
            file.write(json.dumps(output))
            file.flush()


def final_send_environment(sm, env):
    with lock:
        with open(file_path, "w") as file:
            output = {
                "state": "END",
                "loc": sm.loc,
                "RW6L": env["RW6L_lights"],
                "RW6R": env["RW6R_lights"],
                "approach": env["approach_lights"],
                "taxiway": env["taxiway_lights"],
                "fuel_depot": env["fuel_depot_light"],
                "beacon": env["beacon_light"],
                "gate_open": env["gate_open"],
                "day": sm.day,
                "voice_file": sm.voiceComm,
                "flight_id": sm.current_flight_id,
                "mode": sm.mode
            }
            file.write(json.dumps(output))
            file.flush()

    print("simulation over")