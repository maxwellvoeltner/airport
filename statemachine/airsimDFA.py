from statemachine import StateMachine, State
from config import competition_state_times
from time import time, sleep
from filelock import FileLock

class Airsim(StateMachine):

    # only thing I added to this class was the state_entry_time
    def __init__(self, flight_num="Air123", day=1, voiceComm="0.0", RW6L_Lights=0, RW6R_lights=0, RW6L_Approach=0, RW6L_VASI=0, Taxiway_lights=0,
                 Ramp_lights=0, fuel_depot=0, beacon_lights=0, perimeter_breach=False,
                s0_min=1, s1_min=1, s2_min=1, s3_min=1, s4_min=1, s5_min=1, s6_min=1, s7_min=1, s8_min=1, s9_min=1, s10_min=1, s11_min=1, s12_min=1,
                s13_min=1, s14_min=1, s15_min=1, s16_min=1, s17_min=1, s18_min=1, s19_min=1, s20_min=1, s21_min=1, s22_min=1, s23_min=1, s24_min=1,
                holding_min=1, model=None, state_field="state", start_value=None, rtc=True, allow_event_without_transition=False, listeners=None):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition, listeners)

        self.state_entry_time = time()

        # global variables (set to defaults) representing the input
        self.flight_num = flight_num
        self.day = day
        self.voiceComm = voiceComm
        self.loc = 0
        self.RW6L_lights = RW6L_Lights
        self.RW6R_lights = RW6R_lights
        self.RW6L_Approach = RW6L_Approach
        self.RW6L_VASI = RW6L_VASI
        self.Taxiway_lights = Taxiway_lights
        self.Ramp_lights = Ramp_lights
        self.TowerCommFileNum  = 0
        self.fuel_depot = fuel_depot
        self.beacon_lights = beacon_lights
        self.RF_jamming = 0
        self.perimeter_breach = perimeter_breach
        self.s0_min = s0_min
        self.s1_min = s1_min
        self.s2_min = s2_min
        self.s3_min = s3_min
        self.s4_min = s4_min
        self.s5_min = s5_min
        self.s6_min = s6_min
        self.s7_min = s7_min
        self.s8_min = s8_min
        self.s9_min = s9_min
        self.s10_min = s10_min
        self.s11_min = s11_min
        self.s12_min = s12_min
        self.s13_min = s13_min
        self.s14_min = s14_min
        self.s15_min = s15_min
        self.s16_min = s16_min
        self.s17_min = s17_min
        self.s18_min = s18_min
        self.s19_min = s19_min
        self.s20_min = s20_min
        self.s21_min = s21_min
        self.s22_min = s22_min
        self.s23_min = s23_min
        self.s24_min = s24_min
        self.holding_min = holding_min

    # states declaration
    state_zero = State("state_zero", initial=True)
    state_one = State("state_one")
    state_two = State("state_two")
    state_three = State("state_three")
    state_four = State("state_four")
    state_five = State("state_five")
    state_six = State("state_six")
    state_seven = State("state_seven")
    state_eight = State("state_eight")
    state_nine = State("state_nine")
    state_ten = State("state_ten")
    state_eleven = State("state_eleven")
    state_twelve = State("state_twelve")
    state_thirteen = State("state_thirteen")
    state_fourteen = State("state_fourteen")
    state_fifteen = State("state_fifteen")
    state_sixteen = State("state_sixteen")
    state_seventeen = State("state_seventeen")
    state_eighteen = State("state_eighteen")
    state_nineteen = State("state_nineteen")
    state_twenty = State("state_twenty")
    state_twenty_one = State("state_twenty_one")
    state_twenty_two = State("state_twenty_two")
    state_twenty_three = State("state_twenty_three")
    state_twenty_four = State("state_twenty_four")
    state_twenty_five = State("state_twenty_five")
    state_twenty_six = State("state_twenty_six")
    state_twenty_seven = State("state_twenty_seven")
    state_twenty_eight = State("state_twenty_eight")

    # seeing if its been 3 seconds since we got to current state
    def can_state_zero_advance(self):
        return (time() - self.state_entry_time) >= self.s0_min
    
    def can_state_one_advance(self):
        return (time() - self.state_entry_time) >= self.s1_min

    def can_state_two_advance(self):
        return (time() - self.state_entry_time) >= self.s2_min

    def can_state_three_advance(self):
        return (time() - self.state_entry_time) >= self.s3_min

    def can_state_four_advance(self):
        return (time() - self.state_entry_time) >= self.s4_min

    def can_state_five_advance(self):
        return (time() - self.state_entry_time) >= self.s5_min

    def can_state_six_advance(self):
        return (time() - self.state_entry_time) >= self.s6_min

    def can_state_seven_advance(self):
        return (time() - self.state_entry_time) >= self.s7_min

    def can_state_eight_advance(self):
        return (time() - self.state_entry_time) >= self.s8_min

    def can_state_nine_advance(self):
        return (time() - self.state_entry_time) >= self.s9_min

    def can_state_ten_advance(self):
        return (time() - self.state_entry_time) >= self.s10_min

    def can_state_eleven_advance(self):
        return (time() - self.state_entry_time) >= self.s11_min

    def can_state_twelve_advance(self):
        return (time() - self.state_entry_time) >= self.s12_min

    def can_state_thirteen_advance(self):
        return (time() - self.state_entry_time) >= self.s13_min

    def can_state_fourteen_advance(self):
        return (time() - self.state_entry_time) >= self.s14_min

    def can_state_fifteen_advance(self):
        return (time() - self.state_entry_time) >= self.s15_min

    def can_state_sixteen_advance(self):
        return (time() - self.state_entry_time) >= self.s16_min

    def can_state_seventeen_advance(self):
        return (time() - self.state_entry_time) >= self.s17_min

    def can_state_eighteen_advance(self):
        return (time() - self.state_entry_time) >= self.s18_min

    def can_state_nineteen_advance(self):
        return (time() - self.state_entry_time) >= self.s19_min

    def can_state_twenty_advance(self):
        return (time() - self.state_entry_time) >= self.s20_min

    def can_state_twenty_one_advance(self):
        return (time() - self.state_entry_time) >= self.s21_min

    def can_state_twenty_two_advance(self):
        return (time() - self.state_entry_time) >= self.s22_min

    def can_state_twenty_three_advance(self):
        return (time() - self.state_entry_time) >= self.s23_min

    def can_state_twenty_four_advance(self):
        return (time() - self.state_entry_time) >= self.s24_min

    def can_holding_advance(self):
        return (time() - self.state_entry_time) >= self.holding_min

    
    # State to state transitions w/ conditions
    state_zero_to_state_one = state_zero.to(state_one)
    state_zero_to_state_one.add_event("clear")
    state_zero_to_state_one.cond(can_state_one_advance)

    state_one_to_state_two = state_one.to(state_two)
    state_one_to_state_two.add_event("clear")
    state_one_to_state_two.cond(can_state_two_advance)

    state_two_to_state_three = state_two.to(state_three)
    state_two_to_state_three.add_event("clear")
    state_two_to_state_three.cond(can_state_three_advance)

    state_three_to_state_four = state_three.to(state_four)
    state_three_to_state_four.add_event("clear")
    state_three_to_state_four.cond(can_state_four_advance)
    # going into holding pattern
    state_three_to_state_twenty_five = state_three.to(state_twenty_five)
    state_three_to_state_twenty_five.add_event("holding")

    state_four_to_state_five = state_four.to(state_five)
    state_four_to_state_five.add_event("clear")
    state_four_to_state_five.cond(can_state_five_advance)
    # going into holding pattern
    state_four_to_state_twenty_five = state_four.to(state_twenty_five)
    state_four_to_state_twenty_five.add_event("holding")

    state_five_to_state_six = state_five.to(state_six)
    state_five_to_state_six.add_event("clear")
    state_five_to_state_six.cond(can_state_six_advance)
    # going into holding pattern
    state_five_to_state_twenty_five = state_five.to(state_twenty_five)
    state_five_to_state_twenty_five.add_event("holding")

    state_six_to_state_seven = state_six.to(state_seven)
    state_six_to_state_seven.add_event("clear")
    state_six_to_state_seven.cond(can_state_seven_advance)
    # going into holding pattern
    state_six_to_state_twenty_five = state_six.to(state_twenty_five)
    state_six_to_state_twenty_five.add_event("holding")

    state_seven_to_state_eight = state_seven.to(state_eight)
    state_seven_to_state_eight.add_event("clear")
    state_seven_to_state_eight.cond(can_state_eight_advance)

    state_eight_to_state_nine = state_eight.to(state_nine)
    state_eight_to_state_nine.add_event("clear")
    state_eight_to_state_nine.cond(can_state_nine_advance)

    state_nine_to_state_ten = state_nine.to(state_ten)
    state_nine_to_state_ten.add_event("clear")
    state_nine_to_state_ten.cond(can_state_ten_advance)

    state_ten_to_state_eleven = state_ten.to(state_eleven)
    state_ten_to_state_eleven.add_event("clear")
    state_ten_to_state_eleven.cond(can_state_eleven_advance)

    state_eleven_to_state_twelve = state_eleven.to(state_twelve)
    state_eleven_to_state_twelve.add_event("clear")
    state_eleven_to_state_twelve.cond(can_state_twelve_advance)

    state_twelve_to_state_thirteen = state_twelve.to(state_thirteen)
    state_twelve_to_state_thirteen.add_event("clear")
    state_twelve_to_state_thirteen.cond(can_state_thirteen_advance)

    state_thirteen_to_state_fourteen = state_thirteen.to(state_fourteen)
    state_thirteen_to_state_fourteen.add_event("clear")
    state_thirteen_to_state_fourteen.cond(can_state_fourteen_advance)

    state_fourteen_to_state_fifteen = state_fourteen.to(state_fifteen)
    state_fourteen_to_state_fifteen.add_event("clear")
    state_fourteen_to_state_fifteen.cond(can_state_fifteen_advance)

    state_fifteen_to_state_sixteen = state_fifteen.to(state_sixteen)
    state_fifteen_to_state_sixteen.add_event("clear")
    state_fifteen_to_state_sixteen.cond(can_state_sixteen_advance)

    state_sixteen_to_state_seventeen = state_sixteen.to(state_seventeen)
    state_sixteen_to_state_seventeen.add_event("clear")
    state_sixteen_to_state_seventeen.cond(can_state_seventeen_advance)

    state_seventeen_to_state_eighteen = state_seventeen.to(state_eighteen)
    state_seventeen_to_state_eighteen.add_event("clear")
    state_seventeen_to_state_eighteen.cond(can_state_eighteen_advance)

    state_eighteen_to_state_nineteen = state_eighteen.to(state_nineteen)
    state_eighteen_to_state_nineteen.add_event("clear")
    state_eighteen_to_state_nineteen.cond(can_state_nineteen_advance)

    state_nineteen_to_state_twenty = state_nineteen.to(state_twenty)
    state_nineteen_to_state_twenty.add_event("clear")
    state_nineteen_to_state_twenty.cond(can_state_twenty_advance)

    state_twenty_to_state_twenty_one = state_twenty.to(state_twenty_one)
    state_twenty_to_state_twenty_one.add_event("clear")
    state_twenty_to_state_twenty_one.cond(can_state_twenty_one_advance)

    state_twenty_one_to_state_twenty_two = state_twenty_one.to(state_twenty_two)
    state_twenty_one_to_state_twenty_two.add_event("clear")
    state_twenty_one_to_state_twenty_two.cond(can_state_twenty_two_advance)

    state_twenty_two_to_state_twenty_three = state_twenty_two.to(state_twenty_three)
    state_twenty_two_to_state_twenty_three.add_event("clear")
    state_twenty_two_to_state_twenty_three.cond(can_state_twenty_three_advance)

    state_twenty_three_to_state_twenty_four = state_twenty_three.to(state_twenty_four)
    state_twenty_three_to_state_twenty_four.add_event("clear")
    state_twenty_three_to_state_twenty_four.cond(can_state_twenty_four_advance)

    state_twenty_three_to_state_twenty_four = state_twenty_three.to(state_twenty_four)
    state_twenty_three_to_state_twenty_four.add_event("clear")
    state_twenty_three_to_state_twenty_four.cond(can_state_twenty_four_advance)

    # recycle
    state_twenty_four_to_state_zero = state_twenty_four.to(state_zero)
    state_twenty_four_to_state_zero.add_event("clear")
    state_twenty_four_to_state_zero.cond(can_state_twenty_four_advance)

    # holding pattern

    state_twenty_five_to_state_twenty_six = state_twenty_five.to(state_twenty_six)
    state_twenty_five_to_state_twenty_six.add_event("holding")
    state_twenty_five_to_state_twenty_six.cond(can_holding_advance)
    # back to state 3
    state_twenty_five_to_state_three = state_twenty_five.to(state_three)
    state_twenty_five_to_state_three.add_event("clear")

    state_twenty_six_to_state_twenty_seven = state_twenty_six.to(state_twenty_seven)
    state_twenty_six_to_state_twenty_seven.add_event("holding")
    state_twenty_six_to_state_twenty_seven.cond(can_holding_advance)
    # back to state 3
    state_twenty_six_to_state_three = state_twenty_six.to(state_three)
    state_twenty_six_to_state_three.add_event("clear")

    state_twenty_seven_to_state_twenty_eight = state_twenty_seven.to(state_twenty_eight)
    state_twenty_seven_to_state_twenty_eight.add_event("holding")
    state_twenty_seven_to_state_twenty_eight.cond(can_holding_advance)
    # back to state 3
    state_twenty_seven_to_state_three = state_twenty_seven.to(state_three)
    state_twenty_seven_to_state_three.add_event("clear")

    state_twenty_eight_to_state_twenty_five = state_twenty_eight.to(state_twenty_five)
    state_twenty_eight_to_state_twenty_five.add_event("holding")
    state_twenty_eight_to_state_twenty_five.cond(can_holding_advance)
    # back to state 3
    state_twenty_eight_to_state_three = state_twenty_eight.to(state_three)
    state_twenty_eight_to_state_three.add_event("clear")

    
    # when a state is transitioned to, the enter function for the state runs
    # note - eventually the state machine field modifiers need to be changed to output bit setters

    def on_enter_state_zero(self):
        self.state_entry_time = time()
        self.loc = 0 # top-left off the screen
        print("State 0")

    def on_exit_state_zero(self):
        if (self.day == 0): # all lights are on during the night
            self.RW6L_lights = 1
            self.RW6L_Approach = 1
            self.RW6L_VASI = 1
            self.Taxiway_lights = 1
            self.Ramp_lights = 1
            self.RW6R_lights = 1
            self.beacon_lights = 1
        else: # lights are only used when in use during the day
            self.RW6L_lights = 0
            self.RW6L_Approach = 0
            self.RW6L_VASI = 0
            self.Taxiway_lights = 0
            self.Ramp_lights = 0
            self.RW6R_lights = 0
            self.beacon_lights = 0

    def on_enter_state_one(self):
        self.state_entry_time = time()
        self.loc = 1 # top left over the sea (landing sequence - 1/7)
        self.voiceComm = "1.0"
        print("State 1")

    def on_enter_state_two(self):
        self.state_entry_time = time()
        self.loc = 2 # over the sea (landing sequence - 2/7)
        self.voiceComm = "2.0"
        print("State 2")

    def on_exit_state_two(self): # turning on lights for landing assistance
        self.RW6L_Approach = 1
        self.RW6L_VASI = 1
        self.RW6L_lights = 1

    def on_enter_state_three(self):
        self.state_entry_time = time()
        self.loc = 3 # middle left over the sea (landing sequence - 3/7)
        self.voiceComm = "3.0"
        print("State 3")

    def on_enter_state_four(self):
        self.state_entry_time = time()
        self.loc = 4 # middle left over the sea (landing sequence - 4/7)
        self.voiceComm = "4.0"
        print("State 4")

    def on_enter_state_five(self):
        self.state_entry_time = time()
        self.loc = 5 # bottom left over the sea (landing sequence - 5/7)
        self.voiceComm = "5.0"
        print("State 5")

    def on_enter_state_six(self):
        self.state_entry_time = time()
        self.loc = 6 # infront of landing (left) runway (landing sequence - 6/7)
        self.voiceComm = "6.0"
        print("State 6")

    def on_exit_state_six(self):
        if (self.day == 1): # approach lights and VASI turn off when not in use during the day
            self.RW6L_Approach = 0
            self.RW6L_VASI = 0

    def on_enter_state_seven(self):
        self.state_entry_time = time()
        self.loc = 7 # bottom of landing (left) runway (landing sequence - 7/7)
        self.voiceComm = "7.0"
        print("State 7")

    def on_enter_state_eight(self):
        self.state_entry_time = time()
        self.loc = 8 # middle of landing (left) runway
        self.voiceComm = "8.0"
        print("State 8")

    def on_enter_state_nine(self):
        self.state_entry_time = time()
        self.loc = 9 # upper-middle of landing (left) runway (fueling state)
        self.voiceComm = "9.0"
        print("State 9")

    def on_exit_state_nine(self):
        self.Taxiway_lights = 1 # turning on taxiway lights for next sequence
        if (self.day == 1): # runway lights turn off when not in use during the day
            self.RW6L_lights = 0

    def on_enter_state_ten(self):
        self.state_entry_time = time()
        self.loc = 10 # top left of upper taxiway route (taxiway sequence 1 - 1/2)
        self.voiceComm = "10.0"
        print("State 10")

    def on_enter_state_eleven(self):
        self.state_entry_time = time()
        self.loc = 11 # top middle of upper taxiway route (taxiway sequence 1 - 2/2)
        self.voiceComm = "11.0"
        print("State 11")

    def on_exit_state_eleven(self):
        if (self.day == 1): # taxiway lights turn off when not in use during the day
            self.Taxiway_lights = 0
        self.Ramp_lights = 1

    def on_enter_state_twelve(self):
        self.state_entry_time = time()
        self.loc = 12 # top of ramp (ramp sequence - 1/4)
        self.voiceComm = "12.0"
        print("State 12")

    def on_enter_state_thirteen(self):
        self.state_entry_time = time()
        self.loc = 13 # approaching passenger boarding bridge (ramp sequence - 2/4)
        self.voiceComm = "14.0"
        #effectSound("engines_to_off")
        print("State 13")

    def on_enter_state_fourteen(self):
        self.state_entry_time = time()
        self.loc = 14 # stationed at passenger boarding bridge (ramp sequence - 3/4)
        self.voiceComm = "15.0"
        print("State 14")

    def on_enter_state_fifteen(self):
        self.state_entry_time = time()
        self.loc = 15 # exiting ramp (ramp sequence - 4/4)
        self.voiceComm = "21.0"
        print("State 15")

    def on_exit_state_fifteen(self):
        if (self.day == 1): # ramp lights turn of when not in use during the day
            self.Ramp_lights = 0
        self.Taxiway_lights = 1 # turning on taxiway lights for next sequence

    def on_enter_state_sixteen(self):
        self.state_entry_time = time()
        self.loc = 16 # top of taxiway (taxiway sequence 2 - 1/4)
        self.voiceComm = "22.0"
        print("State 16")

    def on_enter_state_seventeen(self):
        self.state_entry_time = time()
        self.loc = 17 # middle of taxiway (taxiway sequence 2 - 2/4)
        self.voiceComm = "23.0"
        #effectSound("engines_to_off");
        print("State 17")

    def on_enter_state_eighteen(self):
        self.state_entry_time = time()
        self.loc = 18 # bottom-right of taxiway (taxiway sequence 2 - 3/4)
        self.voiceComm = "24.0"
        print("State 18")

    def on_enter_state_nineteen(self):
        self.state_entry_time = time()
        self.loc = 19 # bottom-left of taxiway (taxiway sequence 2 - 4/4)
        self.voiceComm = "25.0"
        print("State 19")

    def on_exit_state_nineteen(self):
        if (self.day == 1): # taxiway lights turn off when not in use during the day
            self.Taxiway_lights = 0
        self.RW6R_lights = 1 # turning on departing-runway lights for next sequence

    def on_enter_state_twenty(self):
        self.state_entry_time = time()
        self.loc = 20
        self.voiceComm = "26.0"
        print("State 20")

    def on_enter_state_twenty_one(self):
        self.state_entry_time = time()
        self.loc = 21
        self.voiceComm = "0.0"
        print("State 21")

    def on_enter_state_twenty_two(self):
        self.state_entry_time = time()
        self.loc = 22
        self.voiceComm = "0.0"
        print("State 22")

    def on_exit_state_twenty_two(self):
        if (self.day == 1): # runway lights turn off when not in use during the day
            self.RW6R_lights = 0

    def on_enter_state_twenty_three(self):
        self.state_entry_time = time()
        self.loc = 23
        self.voiceComm = "0.0"
        print("State 23")

    def on_enter_state_twenty_four(self):
        self.state_entry_time = time()
        self.loc = 24
        self.voiceComm = "0.0"
        print("State 24")

    def on_enter_state_twenty_five(self):
        self.state_entry_time = time()
        self.loc = 25
        self.voiceComm = "0.0"
        self.RW6L_lights = 0
        print("State 25: holding pattern (1/4)")

    def on_enter_state_twenty_six(self):
        self.state_entry_time = time()
        self.loc = 26
        self.voiceComm = "0.0"
        print("State 26: holding pattern (2/4)")

    def on_enter_state_twenty_seven(self):
        self.state_entry_time = time()
        self.loc = 27
        self.voiceComm = "0.0"
        print("State 27: holding pattern (3/4)")

    def on_enter_state_twenty_eight(self):
        self.state_entry_time = time()
        self.loc = 28
        self.voiceComm = "0.0"
        print("State 28: holding pattern (4/4)")


# event checkers

# checks if airport has conditions for plane to advance the landing strip (rw6l lights), taxiway (taxiway lights), ramp (ramp lights), or runway (rw6r)
def check_can_advance_runway(day, lights):
    if (day == 1 or lights == 1):
        return True
    else:
        return False

# checks if airport has conditions for plane to land
def check_can_land(jamming, day, appch, vasi, rw6l):
    if (jamming == 0 and (day == 1 or (appch == 1 and vasi == 1 and rw6l == 1))):
        return True
    else:
        return False

# check if airport has conditions for plane to fuel
def check_can_fuel(day, rw6l, depot_lights):
    if (check_can_advance_runway(day, rw6l) and depot_lights == 1):
        return True
    else:
        return False

# check if airport has conditions for plane to depart
def check_can_depart(jamming, day, rw6r):
    if (jamming == 0 and check_can_advance_runway(day, rw6r)):
        return True
    else:
        return False

# running the DFA

if __name__ == "__main__" :

    mode = input("Enter Mode\n1 for demo\n2 for competition\n")

    # instantiate Airsim DFA
    sm = None
    if (mode == '1'):
        # asking for day or night
        day_input = input("Enter 1 for day or 0 for night\n")
        if (day_input != "0" and day_input != "1"): # defaulting to day when given erroneous input
            day_input = 1
        sm = Airsim(day=int(day_input))

    else:  # instantiate the Airsim object with the values from the competition_state_times from the config file
        sm = Airsim(
        s0_min=competition_state_times["s0_min"], s1_min=competition_state_times["s1_min"], s2_min=competition_state_times["s2_min"],
        s3_min=competition_state_times["s3_min"], s4_min=competition_state_times["s4_min"], s5_min=competition_state_times["s5_min"],
        s6_min=competition_state_times["s6_min"], s7_min=competition_state_times["s7_min"], s8_min=competition_state_times["s8_min"],
        s9_min=competition_state_times["s9_min"], s10_min=competition_state_times["s10_min"], s11_min=competition_state_times["s11_min"],
        s12_min=competition_state_times["s12_min"], s13_min=competition_state_times["s13_min"], s14_min=competition_state_times["s14_min"],
        s15_min=competition_state_times["s15_min"], s16_min=competition_state_times["s16_min"], s17_min=competition_state_times["s17_min"],
        s18_min=competition_state_times["s18_min"], s19_min=competition_state_times["s19_min"], s20_min=competition_state_times["s20_min"],
        s21_min=competition_state_times["s21_min"], s22_min=competition_state_times["s22_min"], s23_min=competition_state_times["s23_min"],
        s24_min=competition_state_times["s24_min"], holding_min=competition_state_times["holding_min"]
        )


    # loop that runs the DFA
    while True:

        # get input values from physical airport

        # send state information to the display driver input file

        # File paths and lock
        file_path = "./output.txt"
        lock = FileLock(f"{file_path}.lock")

        with lock:
            with open(file_path, "w") as file:
                line = f"{sm.current_state.name},{sm.loc},{sm.RW6L_lights}{sm.RW6R_lights}{sm.RW6L_Approach}{sm.RW6L_VASI}{sm.Taxiway_lights}{sm.Ramp_lights}{sm.fuel_depot}{sm.beacon_lights},{sm.day},{sm.voiceComm},{sm.flight_num}"
                file.write(line)
                file.flush()

        # demo mode
        # (forces a normal path - will ignore input if connected)
        if (mode == '1'):

            # the event "clear" triggers any transition on the regular path
            try:
                sm.send("clear")
            except:
                pass

        # competition mode
        else:

            # getting current state to determine which check(s) should be done (to avoid doing all the checks so we can save time)
            current_state = sm.current_state.name

            # states 0 - 2, 23, and 24 will always transition to next state after their associated time condition is met
            if (current_state in ["state_zero", "state_one", "state_two", "state_twenty_three,", "state_twenty_four"]):
                try:
                    sm.send("clear")
                except:
                    pass
            
            # states 3 - 6 (normal path over the sea) and 25 - 28 (holding pattern) need the airport to have the "can-land" condition satisfied in order to transition
            elif (current_state in ["state_three", "state_four", "state_five", "state_six", "state_twenty_five", "state_twenty_six", "state_twenty_seven", "state_twenty_eight"]):
                #print(check_can_land(sm.RF_jamming, sm.day, sm.RW6L_Approach, sm.RW6L_VASI, sm.RW6L_lights))
                if (check_can_land(sm.RF_jamming, sm.day, sm.RW6L_Approach, sm.RW6L_VASI, sm.RW6L_lights)):
                    try:
                        sm.send("clear")
                    except:
                        pass
                else:
                    try:
                        sm.send("holding")
                    except:
                        pass
            
            # states 7 and 8 need the airport to have the "can-advance-runway" condition satisfied in order to transition
            elif (current_state in ["state_seven", "state_eight"]):
                if (check_can_advance_runway(sm.day, sm.RW6L_lights)):
                    try:
                        sm.send("clear")
                    except:
                        pass
            
            # state 9 needs the airport to have the "can-fuel" condition satisfied in order to transition
            elif (current_state == "state_nine"):
                if (check_can_fuel(sm.day, sm.RW6L_lights, sm.fuel_depot)):
                    try:
                        sm.send("clear")
                    except:
                        pass

            # states 10, 11 and 16 - 19 need the airport to have the "can-advance-runway" (arguments adjusted for taxiway) condition satisfied in order to transition
            elif (current_state in ["state_ten", "state_eleven", "state_sixteen", "state_seventeen", "state_eighteen", "state_nineteen"]):
                if (check_can_advance_runway(sm.day, sm.Taxiway_lights)):
                    try:
                        sm.send("clear")
                    except:
                        pass

            # states 12 - 15 need the airport to have the "can-advance-runway" (arguments adjusted for ramp) condition satisfied in order to transition
            elif (current_state in ["state_twelve", "state_thirteen", "state_fourteen", "state_fifteen"]):
                if (check_can_advance_runway(sm.day, sm.Ramp_lights)):
                    try:
                        sm.send("clear")
                    except:
                        pass
            
            # states 20 - 22 need the airport to have the "can-depart" condition satisfied in order to transition
            elif (current_state in ["state_twenty", "state_twenty_one", "state_twenty_two"]):
                if (check_can_depart(sm.RF_jamming, sm.day, sm.RW6R_lights)):
                    try:
                        sm.send("clear")
                    except:
                        pass
            else:
                try:
                    sm.send("clear")
                except:
                    pass

        sleep(1)