from statemachine import StateMachine, State
from time import time, sleep

class Airplane(StateMachine):

    # only thing I added to this class was the state_entry_time
    def __init__(self, voiceComm, loc, RW6L_Lights, RW6R_lights, RW6L_Approach, RW6L_VASI, Taxiway_lights, Ramp_lights, FuelDepot_lights,
                 s0_min, s1_min, s2_min,
                 model = None, state_field = "state", start_value = None, rtc = True, allow_event_without_transition = False, listeners = None):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition, listeners)
        self.state_entry_time = time()
        # global variables (set to defaults) representing the input
        self.voiceComm = voiceComm
        self.loc = loc
        self.RW6L_lights = RW6L_Lights
        self.RW6R_lights = RW6R_lights
        self.RW6L_Approach = RW6L_Approach
        self.RW6L_VASI = RW6L_VASI
        self.Taxiway_lights = Taxiway_lights
        self.Ramp_lights = Ramp_lights
        self.TowerCommFileNum  = 0
        self.FuelDepot_lights = FuelDepot_lights
        self.RF_jamming = 0
        self.s0_min = s0_min
        self.s1_min = s1_min
        self.s2_min = s2_min

    # states declaration
    state_zero = State("state_zero", initial=True)
    state_one = State("state_one")
    state_two = State("state_two", final=True)

    # seeing if its been 3 seconds since we got to current state
    def can_state_zero_advance(self):
        return (time() - self.state_entry_time) >= self.s0_min
    
    def can_state_one_advance(self):
        return (time() - self.state_entry_time) >= self.s1_min

    def can_state_two_advance(self):
        return (time() - self.state_entry_time) >= self.s2_min
  
    # State to state transitions w/ conditions
    state_zero_to_state_one = state_zero.to(state_one)
    state_zero_to_state_one.add_event("clear")
    state_zero_to_state_one.cond(can_state_one_advance)

    state_one_to_state_two = state_one.to(state_two)
    state_one_to_state_two.add_event("clear")
    state_one_to_state_two.cond(can_state_two_advance)

    '''
    the state machine recognizes which functions to execute because it reads for:

        on_exit_[insert current state]
        on_enter_[insert current state]

    so the enter and exit functions get called automatically which is cool (so long as you follow the format)

    not totally necessary (except for the entry time)
    nice if we need it
    '''

    def on_enter_state_zero(self):
        self.state_entry_time = time()
        self.loc = 0
        print("Startin off at state 0")

    def on_enter_state_one(self):
        self.state_entry_time = time()
        self.loc = 0
        print("Hoppin into state 1")

    def on_enter_state_two(self):
        self.state_entry_time = time()
        self.loc = 0
        print("Jumpin into state 2")


# running the DFA

if __name__ == "__main__" :

    # get initial input

    # start-up the DFA with input (randoms I put in)
    sm = Airplane("0.0", 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3)

    # loop that runs the DFA
    while True:

        # get input values

        # we would evaluate the input situation
        '''
        if (!RW6L_lights or !RW6R_lights or !RW6L_Approach or !RW6L_VASI or !Taxiway_lights or !Ramp_lights):
            try:
                sm.send("light-problem")
            except:
                pass
        else:
            try:
                sm.send("lights-working")
            except:
                pass
                
        if (!RF_jamming)
            try:
                sm.send("RF-jammed")
            except:
                pass
        '''

        try:
            sm.send("clear")
        except:
            pass
        
        sleep(1)