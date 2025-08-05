Inputs 

Mark mentioned the following inputs for the DFA: 

    BEACON – the beacon 

    APPROACH – approach lights & VASI (constructed by Mark as parts of one whole component) 

    RW6L – the lights on the left runway 

    TAXIWAY – the taxiway lights 

    RW6R – the lights on the right runway 

    FUEL – operation status of the fuel station 

    GATE – "perimeter breach" 

    Gate closed → perimeter breach = 0 

    Gate open → perimeter breach = 1 

    VOICECOMM – voice jamming or not 

    SCALE – "calibration okay" (not a Boolean) 

    Input of 1 → calibration okay = 1 

    Input of 0 → calibration okay = 0 

These inputs are considered in the DFA setup.


DFA Setup 

    States are instantiated. 

    Transitions are defined. 

    States are linked: 

    Example: state_one_to_state_two = state_one.to(state_two) 

    Events are associated with transitions: 

    Example: state_one_to_state_two.add_event("clear") 

    Conditions are applied to transitions. The transition only occurs if the condition is satisfied: 

    Example: state_one_to_state_two.cond(*time_function_for_state_one) 

    Functions for entering and exiting states are defined (see the "Transition Process" section below).


General Overview of How the DFA Works 

Part I: Choosing a Mode 

    DEMO Mode: 

    Type "python3 driver.py" for DEMO mode. 

    The DFA is instantiated with flights from the flight database and the default minimum transition times for each state (1 second). 

    COMPETITION Mode: 

    Type "python3 driver.py competition" for COMPETITION mode. 

    The DFA is instantiated with flights from the flight database and the minimum transition times specified in the competition_state_times dictionary in the config file. 

    Minimum transition time is the minimum time the DFA must stay in one state to transition to another state.


Part II: Start of the Loop 

    The DFA receives input from the physical airport through the airio server. 

    The DFA sends relevant attribute values (e.g., RW6L lights) to a file for the display driver.


Part III: Triggering State Transitions 

    DEMO Mode: 

    Forces a transition to the next state by sending the event "clear." 

    COMPETITION Mode: 

    Based on the current state, a check is performed to see if the airport has the conditions necessary for the transition. 

    Most states only have one transition, to the next state in the normal path. If the check passes, the event "clear" is sent and the DFA transitions. If the check fails, the DFA stays in its current state. 

    States 3-6 (approach states): 

    These states have an additional connection to state 25 (the first state of the holding pattern). 

    If the check doesn’t pass, the event "holding" is sent and the DFA transitions to state 25. 

    States in the holding pattern follow the same check process. If the check passes, the DFA transitions back to state 3; otherwise, the DFA stays in the holding pattern (states 25-28). 


Transition Process 

    Triggering a Transition: 

    When an event triggers a transition and the condition is met, a transition occurs. 

    Functions on Transition:

    Each state may have an on_enter and on_exit function. 

    The on_exit function for the current state runs first. 

    Then, the on_enter function for the next state runs. 

    Most states have an on_enter function, and some have an on_exit function. 

 
Notes on Transition Failures 

    If a transition fails, a TransitionNotAllowed error will occur. This can happen for two reasons: 

    The event was sent in a state that does not have a transition.

    The on_exit or on_enter function raised an error.

    This is why all event sending is wrapped in try/except blocks. If a transition fails, the program just continues without transitioning.