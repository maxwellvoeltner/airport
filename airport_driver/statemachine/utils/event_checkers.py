# event checkers

# checks if airport has conditions for plane to advance the landing strip (rw6l lights), taxiway (taxiway lights), or runway (rw6r)
def check_can_advance_runway(day, lights, gate_open):
    if ((day or lights) and (not gate_open)):
        return True
    else:
        return False

# checks if airport has conditions for plane to land
def check_can_land(day, beacon, appch, rw6l, gate_open):
    if ((day or (appch and rw6l and beacon)) and (not gate_open)):
        return True
    else:
        return False

# check if airport has conditions for plane to fuel
def check_can_fuel(day, rw6l, depot_lights, gate_open):
    if (check_can_advance_runway(day, rw6l, gate_open) and depot_lights):
        return True
    else:
        return False

def check_can_advance_ramp(gate_open):
    if (not gate_open):
        return True
    else:
        return False