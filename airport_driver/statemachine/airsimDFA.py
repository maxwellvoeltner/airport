from statemachine import StateMachine, State
import utils.state_transition_aux as state_transition_aux
import utils.flight_delay_aux as flight_delay_aux

class Airsim( StateMachine ):

    def __init__(self, mode="demo", alcms_client=None, fuel_client=None, gate_client=None, starting_minutes=0, minutes_per_loop=1, time_to_arrive_from_s0=6, flight_list=["BWI"],
                model=None, state_field="state", start_value=None, rtc=True, allow_event_without_transition=False, listeners=None, **state_times):

        self.mode = mode
        self.alcms_client = alcms_client
        self.fuel_client = fuel_client
        self.gate_client = gate_client
        self.loop_num = 0 # tracks the number of loops the simulation performs (for demo mode - resets to 0 after all the flights have been cycled through to "restart")
        self.state_entry_loop_num = 0 # used to keep track of how many loop iterations the DFA has been in the current state. It gets updated everytime a new state is enetered.
        self.simulation_minutes = 0
        self.minutes_per_loop = minutes_per_loop
        self.time_to_arrive_from_s0 = time_to_arrive_from_s0
        self.starting_minutes = starting_minutes
        self.flight_list = flight_list # list of the flight names (ex: LAX) from the flight database.
        self.current_flight_index = 0 # tracks the index of the current flight the DFA is on.
        self.current_flight_object = { "sourceAirport": "BWI", "arrivalFlight": "BA2", "arrivalTime": 506, "arrivalStatus": "Scheduled", "departureFlight": "BA1", "departureTime": 592, "departureStatus": "Scheduled", "gate": 1 }
        self.current_flight_id = "BWI"
        self.day = 1 # Daytime/Nighttime: value of 1 indicates daytime and value of 0 indicates nighttime.
        self.loc = 0 # location number of the airplane on the map in the driver.
        for key, value in state_times.items(): # these are all the minimum amount of time the DFA must spend in the state to have the option of transitioning
            setattr(self, key, value)

        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition, listeners)

    # state instantiations
    # normal flight path states (0 - 24)
    state_zero = State("state_zero", initial=True) # top-left off the screen
    state_one = State("state_one") # top left over the sea (landing sequence - 1/7)
    state_two = State("state_two") # over the sea (landing sequence - 2/7)
    state_three = State("state_three") # middle left over the sea (landing sequence - 3/7)
    state_four = State("state_four") # middle left over the sea (landing sequence - 4/7)
    state_five = State("state_five") # bottom left over the sea (landing sequence - 5/7)
    state_six = State("state_six") # in-front of landing (left) runway (landing sequence - 6/7)
    state_seven = State("state_seven") # bottom of landing (left) runway (landing sequence - 7/7)
    state_eight = State("state_eight") # middle of landing (left) runway
    state_nine = State("state_nine") # upper-middle of landing (left) runway (fueling state)
    state_ten = State("state_ten") # top left of upper taxiway route (taxiway sequence 1 - 1/2)
    state_eleven = State("state_eleven") # top middle of upper taxiway route (taxiway sequence 1 - 2/2)
    state_twelve = State("state_twelve") # top of ramp (ramp sequence - 1/4)
    state_thirteen = State("state_thirteen") # approaching passenger boarding bridge (ramp sequence - 2/4)
    state_fourteen = State("state_fourteen") # stationed at passenger boarding bridge (ramp sequence - 3/4)
    state_fifteen = State("state_fifteen") # exiting ramp (ramp sequence - 4/4)
    state_sixteen = State("state_sixteen") # top of taxiway (taxiway sequence 2 - 1/4)
    state_seventeen = State("state_seventeen") # middle of taxiway (taxiway sequence 2 - 2/4)
    state_eighteen = State("state_eighteen") # bottom-right of taxiway (taxiway sequence 2 - 3/4)
    state_nineteen = State("state_nineteen") # bottom-left of taxiway (taxiway sequence 2 - 4/4)
    state_twenty = State("state_twenty") # bottom of right runway (takeoff sequence 1/4)
    state_twenty_one = State("state_twenty_one") # middle of right runway (takeoff sequence 2/4)
    state_twenty_two = State("state_twenty_two") # top of right runway (takeoff sequence 3/4)
    state_twenty_three = State("state_twenty_three") # above top of right runway (takeoff sequence 4/4)
    state_twenty_four = State("state_twenty_four") # well over the sea above the right runway
    # holding pattern state
    state_twenty_five = State("state_twenty_five") # top right of left sea (holding pattern sequence 1/1)

    # sends an event - the statemachine class makes the program fail if an event is sent and its invalid so the except and pass avoid that
    def send_event(self, event):
        try:
            self.send(event)
            return True
        except:
            return False

    # seeing if its been x loops since we got to current state
    def can_advance(self, index):
        key = f"s{index}_min" if isinstance(index, int) else "holding_min"
        return (self.loop_num - self.state_entry_loop_num) >= getattr(self, key)

    def cancel_outbound_flight(self):
        flight_delay_aux.delay_flights( self ) # accounting for the delays that happened since the last delay_flights function call
        state_transition_aux.update_flight(self.current_flight_id, {"departureTime": -1, "departureStatus": "Cancelled"})
        if (self.current_flight_index == len(self.flight_list) - 1): # resetting the flights statuses if we're ending the last flight's cycle
            state_transition_aux.reset_airplanes()
            self.current_flight_index = 0 # start over with the first flight
        else: # current flight is not the last flight and there were no delays
            self.current_flight_index += 1 # move onto the next flight

    def cancel_inbound_flight(self):
        cancelled_last_flight = (self.current_flight_index == len(self.flight_list) - 1)
        self.cancel_outbound_flight() # we need to keep the current time of the flight for the delay function so we can't overwrite the arrival time yet
        state_transition_aux.update_flight(self.current_flight_id, {"arrivalTime": -1, "arrivalStatus": "Rerouted (Maui)"})
        if cancelled_last_flight: # edge case that the last flight gets rerouted (but the update happens after we reset the airplanes already)
            state_transition_aux.reset_airplanes() # so just reset them again to get the arrival of the last flight set to its time and scheduled

    def exit_holding(self):
        state_transition_aux.update_flight(self.current_flight_id, {"arrivalTime": -1, "arrivalStatus": "En Route"})

    def can_advance_from_state_zero(self):
        arrival_time = self.current_flight_object.get("arrivalTime")
        current_time = self.simulation_minutes
        diff = (arrival_time - current_time)
        return (diff <= self.time_to_arrive_from_s0) and self.can_advance(0) # advancing uninterrupted from the current time will not make the plane arrive early

    def can_advance_from_state_one(self):
        return self.can_advance(1)

    def can_advance_from_state_two(self):
        return self.can_advance(2)

    def can_advance_from_state_three(self):
        return self.can_advance(3)

    def can_advance_from_state_four(self):
        return self.can_advance(4)

    def can_advance_from_state_five(self):
        return self.can_advance(5)

    def can_advance_from_state_six(self):
        return self.can_advance(6)

    def can_advance_from_state_seven(self):
        return self.can_advance(7)

    def can_advance_from_state_eight(self):
        return self.can_advance(8)

    def can_advance_from_state_nine(self):
        return self.can_advance(9)

    def can_advance_from_state_ten(self):
        return self.can_advance(10)

    def can_advance_from_state_eleven(self):
        return self.can_advance(11)

    def can_advance_from_state_twelve(self):
        return self.can_advance(12)

    def can_advance_from_state_thirteen(self):
        return self.can_advance(13)

    def can_advance_from_state_fourteen(self):
        return self.can_advance(14)

    def can_advance_from_state_fifteen(self):
        return self.can_advance(15)

    def can_advance_from_state_sixteen(self):
        return self.can_advance(16)

    def can_advance_from_state_seventeen(self):
        return self.can_advance(17)

    def can_advance_from_state_eighteen(self):
        return self.can_advance(18)

    def can_advance_from_state_nineteen(self):
        return self.can_advance(19)

    def can_advance_from_state_twenty(self):
        return self.can_advance(20)

    def can_advance_from_state_twenty_one(self):
        return self.can_advance(21)

    def can_advance_from_state_twenty_two(self):
        return self.can_advance(22)

    def can_advance_from_state_twenty_three(self):
        return self.can_advance(23)

    def can_advance_from_state_twenty_four(self):
        return self.can_advance(24)

    def can_advance_from_holding(self):
        return self.can_advance("holding")
    
    
    # State to state transitions w/ conditions
    state_zero_to_state_one = state_zero.to(state_one)
    state_zero_to_state_one.add_event("clear")
    state_zero_to_state_one.cond(can_advance_from_state_zero)

    state_one_to_state_two = state_one.to(state_two)
    state_one_to_state_two.add_event("clear")
    state_one_to_state_two.cond(can_advance_from_state_one)

    state_two_to_state_three = state_two.to(state_three)
    state_two_to_state_three.add_event("clear")
    state_two_to_state_three.cond(can_advance_from_state_two)

    state_three_to_state_four = state_three.to(state_four)
    state_three_to_state_four.add_event("clear")
    state_three_to_state_four.cond(can_advance_from_state_three)
    # holding pattern transition
    state_three_to_state_twenty_five = state_three.to(state_twenty_five)
    state_three_to_state_twenty_five.add_event("holding")

    state_four_to_state_five = state_four.to(state_five)
    state_four_to_state_five.add_event("clear")
    state_four_to_state_five.cond(can_advance_from_state_four)
    # holding pattern transition
    state_four_to_state_twenty_five = state_four.to(state_twenty_five)
    state_four_to_state_twenty_five.add_event("holding")

    state_five_to_state_six = state_five.to(state_six)
    state_five_to_state_six.add_event("clear")
    state_five_to_state_six.cond(can_advance_from_state_five)
    # holding pattern transition
    state_five_to_state_twenty_five = state_five.to(state_twenty_five)
    state_five_to_state_twenty_five.add_event("holding")

    state_six_to_state_seven = state_six.to(state_seven)
    state_six_to_state_seven.add_event("clear")
    state_six_to_state_seven.cond(can_advance_from_state_six)
    # holding pattern transition
    state_six_to_state_twenty_five = state_six.to(state_twenty_five)
    state_six_to_state_twenty_five.add_event("holding")

    state_seven_to_state_eight = state_seven.to(state_eight)
    state_seven_to_state_eight.add_event("clear")
    state_seven_to_state_eight.cond(can_advance_from_state_seven)

    state_eight_to_state_nine = state_eight.to(state_nine)
    state_eight_to_state_nine.add_event("clear")
    state_eight_to_state_nine.cond(can_advance_from_state_eight)

    state_nine_to_state_ten = state_nine.to(state_ten)
    state_nine_to_state_ten.add_event("clear")
    state_nine_to_state_ten.cond(can_advance_from_state_nine)

    state_ten_to_state_eleven = state_ten.to(state_eleven)
    state_ten_to_state_eleven.add_event("clear")
    state_ten_to_state_eleven.cond(can_advance_from_state_ten)

    state_eleven_to_state_twelve = state_eleven.to(state_twelve)
    state_eleven_to_state_twelve.add_event("clear")
    state_eleven_to_state_twelve.cond(can_advance_from_state_eleven)

    state_twelve_to_state_thirteen = state_twelve.to(state_thirteen)
    state_twelve_to_state_thirteen.add_event("clear")
    state_twelve_to_state_thirteen.cond(can_advance_from_state_twelve)

    state_thirteen_to_state_fourteen = state_thirteen.to(state_fourteen)
    state_thirteen_to_state_fourteen.add_event("clear")
    state_thirteen_to_state_fourteen.cond(can_advance_from_state_thirteen)

    state_fourteen_to_state_fifteen = state_fourteen.to(state_fifteen)
    state_fourteen_to_state_fifteen.add_event("clear")
    state_fourteen_to_state_fifteen.cond(can_advance_from_state_fourteen)

    state_fifteen_to_state_sixteen = state_fifteen.to(state_sixteen)
    state_fifteen_to_state_sixteen.add_event("clear")
    state_fifteen_to_state_sixteen.cond(can_advance_from_state_fifteen)

    state_sixteen_to_state_seventeen = state_sixteen.to(state_seventeen)
    state_sixteen_to_state_seventeen.add_event("clear")
    state_sixteen_to_state_seventeen.cond(can_advance_from_state_sixteen)

    state_seventeen_to_state_eighteen = state_seventeen.to(state_eighteen)
    state_seventeen_to_state_eighteen.add_event("clear")
    state_seventeen_to_state_eighteen.cond(can_advance_from_state_seventeen)

    state_eighteen_to_state_nineteen = state_eighteen.to(state_nineteen)
    state_eighteen_to_state_nineteen.add_event("clear")
    state_eighteen_to_state_nineteen.cond(can_advance_from_state_eighteen)

    state_nineteen_to_state_twenty = state_nineteen.to(state_twenty)
    state_nineteen_to_state_twenty.add_event("clear")
    state_nineteen_to_state_twenty.cond(can_advance_from_state_nineteen)

    state_twenty_to_state_twenty_one = state_twenty.to(state_twenty_one)
    state_twenty_to_state_twenty_one.add_event("clear")
    state_twenty_to_state_twenty_one.cond(can_advance_from_state_twenty)

    state_twenty_one_to_state_twenty_two = state_twenty_one.to(state_twenty_two)
    state_twenty_one_to_state_twenty_two.add_event("clear")
    state_twenty_one_to_state_twenty_two.cond(can_advance_from_state_twenty_one)

    state_twenty_two_to_state_twenty_three = state_twenty_two.to(state_twenty_three)
    state_twenty_two_to_state_twenty_three.add_event("clear")
    state_twenty_two_to_state_twenty_three.cond(can_advance_from_state_twenty_two)

    state_twenty_three_to_state_twenty_four = state_twenty_three.to(state_twenty_four)
    state_twenty_three_to_state_twenty_four.add_event("clear")
    state_twenty_three_to_state_twenty_four.cond(can_advance_from_state_twenty_three)

    # recycle
    state_twenty_four_to_state_zero = state_twenty_four.to(state_zero)
    state_twenty_four_to_state_zero.add_event("clear")
    state_twenty_four_to_state_zero.cond(can_advance_from_state_twenty_four)

    # holding pattern back to state 3
    state_twenty_five_to_state_three = state_twenty_five.to(state_three, on="exit_holding")
    state_twenty_five_to_state_three.add_event("clear")

    # cancellation of inbound flight
    state_twenty_five_to_state_zero = state_twenty_five.to(state_zero, on="cancel_inbound_flight")
    state_twenty_five_to_state_zero.add_event("delayed-beyond-limit")

    # cancellation of outgoing flight
    state_seven_to_state_zero = state_seven.to(state_zero, on="cancel_outbound_flight")
    state_seven_to_state_zero.add_event("delayed-beyond-limit")

    state_eight_to_state_zero = state_eight.to(state_zero, on="cancel_outbound_flight")
    state_eight_to_state_zero.add_event("delayed-beyond-limit")

    state_nine_to_state_zero = state_nine.to(state_zero, on="cancel_outbound_flight")
    state_nine_to_state_zero.add_event("delayed-beyond-limit")

    state_ten_to_state_zero = state_ten.to(state_zero, on="cancel_outbound_flight")
    state_ten_to_state_zero.add_event("delayed-beyond-limit")

    state_eleven_to_state_zero = state_eleven.to(state_zero, on="cancel_outbound_flight")
    state_eleven_to_state_zero.add_event("delayed-beyond-limit")

    state_twelve_to_state_zero = state_twelve.to(state_zero, on="cancel_outbound_flight")
    state_twelve_to_state_zero.add_event("delayed-beyond-limit")

    state_thirteen_to_state_zero = state_thirteen.to(state_zero, on="cancel_outbound_flight")
    state_thirteen_to_state_zero.add_event("delayed-beyond-limit")

    state_fourteen_to_state_zero = state_fourteen.to(state_zero, on="cancel_outbound_flight")
    state_fourteen_to_state_zero.add_event("delayed-beyond-limit")

    state_fifteen_to_state_zero = state_fifteen.to(state_zero, on="cancel_outbound_flight")
    state_fifteen_to_state_zero.add_event("delayed-beyond-limit")

    state_sixteen_to_state_zero = state_sixteen.to(state_zero, on="cancel_outbound_flight")
    state_sixteen_to_state_zero.add_event("delayed-beyond-limit")

    state_seventeen_to_state_zero = state_seventeen.to(state_zero, on="cancel_outbound_flight")
    state_seventeen_to_state_zero.add_event("delayed-beyond-limit")

    state_eighteen_to_state_zero = state_eighteen.to(state_zero, on="cancel_outbound_flight")
    state_eighteen_to_state_zero.add_event("delayed-beyond-limit")

    state_nineteen_to_state_zero = state_nineteen.to(state_zero, on="cancel_outbound_flight")
    state_nineteen_to_state_zero.add_event("delayed-beyond-limit")

    state_twenty_to_state_zero = state_twenty.to(state_zero, on="cancel_outbound_flight")
    state_twenty_to_state_zero.add_event("delayed-beyond-limit")

    state_twenty_one_to_state_zero = state_twenty_one.to(state_zero, on="cancel_outbound_flight")
    state_twenty_one_to_state_zero.add_event("delayed-beyond-limit")

    state_twenty_two_to_state_zero = state_twenty_two.to(state_zero, on="cancel_outbound_flight")
    state_twenty_two_to_state_zero.add_event("delayed-beyond-limit")


    def enter_state(self, loc_value):
        # every state entry we have to update the entry loop number, location number
        self.state_entry_loop_num = self.loop_num
        self.loc = loc_value

    def on_enter_state_zero(self):
        self.current_flight_id = self.flight_list[self.current_flight_index] # make the current flight id the name of the airport it's coming from
        self.current_flight_object = state_transition_aux.get_airplane(self.current_flight_id) # updating current flight object # make the current flight num the next (or first if resetting simulation) flight num
        self.loop_num = 0
        self.state_entry_loop_num = 0
        self.loc = 0 # top-left off the screen
        if (self.current_flight_index == 0): # resetting to start time after all 10 airplanes have gone through
            self.simulation_minutes = self.starting_minutes
        print(self.current_flight_id)

    def on_exit_state_zero(self):
        if (self.mode == "demo"):
            action = "ON" if (self.day == 0) else "OFF"
            for light in ["RW6L", "taxiway_lights", "RW6R"]:
                state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, light, action, day_only=False) # turn on/off all light outputs depending on day/night

    def on_enter_state_one(self): # top left over the sea (landing sequence - 1/7)
        self.enter_state(1)
        state_transition_aux.update_flight(self.current_flight_id, {"arrivalStatus": "En Route"})

    def on_enter_state_two(self): # over the sea (landing sequence - 2/7)
        self.enter_state(2)

    def on_exit_state_two(self): # turning on lights for landing assistance
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "RW6L", "ON", day_only=False) # telling airio server to set approach output to turn on approach output

    def on_enter_state_three(self): # middle left over the sea (landing sequence - 3/7)
        self.enter_state(3)

    def on_enter_state_four(self):
        self.enter_state(4) # middle left over the sea (landing sequence - 4/7)

    def on_enter_state_five(self):
        self.enter_state(5) # bottom left over the sea (landing sequence - 5/7)
        state_transition_aux.update_flight(self.current_flight_id, {"arrivalStatus": "On Approach"})

    def on_enter_state_six(self):
        self.enter_state(6) # in-front of landing (left) runway (landing sequence - 6/7)

    def on_exit_state_six(self): # turning off the approach and vasi lights
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "RW6L", "OFF", day_only=True) # telling airio server to turn off approach output

    def on_enter_state_seven(self):
        self.enter_state(7) # bottom of landing (left) runway (landing sequence - 7/7)
        state_transition_aux.update_flight(self.current_flight_id, {"arrivalStatus": "Arrived", "arrivalTime": self.simulation_minutes})

    def on_enter_state_eight(self):
        self.enter_state(8) # middle of landing (left) runway

    def on_enter_state_nine(self):
        self.enter_state(9) # upper-middle of landing (left) runway (fueling state)
    
    def on_exit_state_nine(self):
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "RW6L", "OFF", day_only=True) # telling airio server to turn off left runway lights output
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "taxiway_lights", "ON", day_only=False) # telling airio server to turn on taxi light output

    def on_enter_state_ten(self):
        self.enter_state(10) # top left of upper taxiway route (taxiway sequence 1 - 1/2)

    def on_enter_state_eleven(self):
        self.enter_state(11) # top middle of upper taxiway route (taxiway sequence 1 - 2/2)

    def on_exit_state_eleven(self):
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "taxiway_lights", "OFF", day_only=True) # telling airio server to turn off taxiway lights output

    def on_enter_state_twelve(self):
        self.enter_state(12) # top of ramp (ramp sequence - 1/4)
        state_transition_aux.update_flight(self.current_flight_id, {"departureStatus": "Check-In"})

    def on_enter_state_thirteen(self):
        self.enter_state(13) # approaching passenger boarding bridge (ramp sequence - 2/4)

    def on_enter_state_fourteen(self):
        self.enter_state(f"14.{self.current_flight_object.get('gate')}") # stationed at passenger boarding bridge (ramp sequence - 3/4)
        state_transition_aux.update_flight(self.current_flight_id, {"departureStatus": "Boarding"})

    def on_enter_state_fifteen(self):
        self.enter_state(15) # exiting ramp (ramp sequence - 4/4)
        state_transition_aux.update_flight(self.current_flight_id, {"departureStatus": "Taxiing"})

    def on_exit_state_fifteen(self):
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "taxiway_lights", "ON", day_only=False) # telling airio server to turn on taxiway lights output

    def on_enter_state_sixteen(self):
        self.enter_state(16) # top of taxiway (taxiway sequence 2 - 1/4)

    def on_enter_state_seventeen(self):
        self.enter_state(17) # middle of taxiway (taxiway sequence 2 - 2/4)

    def on_enter_state_eighteen(self):
        self.enter_state(18) # bottom-right of taxiway (taxiway sequence 2 - 3/4)

    def on_enter_state_nineteen(self):
        self.enter_state(19) # bottom-left of taxiway (taxiway sequence 2 - 4/4)

    def on_exit_state_nineteen(self):
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "taxiway_lights", "OFF", day_only=True) # telling airio server to turn off taxiway lights output
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "RW6R", "ON", day_only=False) # telling airio server to turn on right runway lights output

    def on_enter_state_twenty(self):
        self.enter_state(20) # bottom of right runway (takeoff sequence 1/4)
        state_transition_aux.update_flight(self.current_flight_id, {"departureStatus": "On Runway"})

    def on_enter_state_twenty_one(self):
        self.enter_state(21) # middle of right runway (takeoff sequence 2/4)

    def on_enter_state_twenty_two(self):
        self.enter_state(22) # top of right runway (takeoff sequence 3/4)

    def on_exit_state_twenty_two(self):
        state_transition_aux.set_signal(self.mode, self.alcms_client, self.day, "RW6R", "OFF", day_only=True) # telling airio server to turn off right runway lights output

    def on_enter_state_twenty_three(self):
        self.enter_state(23) # above top of right runway (takeoff sequence 4/4)
        state_transition_aux.update_flight(self.current_flight_id, {"departureStatus": "Departed", "departureTime" : self.simulation_minutes})

    def on_enter_state_twenty_four(self):
        self.enter_state(24) # well over the sea above the right runway

    def on_exit_state_twenty_four(self):  
        # resetting the flights statuses if we're ending the last flight's cycle
        if (self.current_flight_index == len(self.flight_list) - 1):
            state_transition_aux.reset_airplanes()
            self.current_flight_index = 0 # start over with the first flight
        else: # current flight is not the last flight and there were no delays
            self.current_flight_index += 1 # move onto the next flight

    def on_enter_state_twenty_five(self):
        self.enter_state(25) # top right of left sea (holding pattern sequence 1/4)
        state_transition_aux.update_flight(self.current_flight_id, {"arrivalStatus": "Holding"})