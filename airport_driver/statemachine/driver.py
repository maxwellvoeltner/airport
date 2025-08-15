import sys, requests
from time import time, sleep
from utils import event_checkers, flight_delay_aux, setup_aux, airport_io, config_validator, file_writing
import config


def run_demo( sm ):
    try:
        while True:
            try:
                t = time()
                # sending current time to the backend database (for the flight board to read and display)
                requests.post( config.simulation_time_url, json={"time": sm.simulation_minutes} )

                # trying to advance to the next state in the normal path
                sm.send_event("clear")

                # updating the environment because the state machine can drive changes to the environment of state changes
                env = airport_io.update_environment( sm )
                
                # sending the environment and relevant flight info to an output file (for the display driver to read and display)
                sleep(max(0, 1 - (time() - t))) # this is for the airplane animation to time up nicely in the display
                file_writing.send_environment( sm, env )

                # loop maintainence
                sm.loop_num += 1 # updating loop number (necessary for state transition logic)
                sm.simulation_minutes = (sm.simulation_minutes + sm.minutes_per_loop)  # updating the sim time in minutes
                print(sm.current_state.name)
                sleep(max(0, 1.1 - (time() - t)))

            except Exception as e:
                print(e)
                pass # incase an error happens from reading or writing just continue

    except KeyboardInterrupt:
        airport_io.handle_exit( sm )


def run_competition( sm ):
    try:
        # setting up the length of time the COMPETITION mode runs for
        start_time = time()
        end_condition = lambda: (time() - start_time) < (config.competition_mode_maximum_time_in_minutes * 60)
        a = start_time
        while end_condition( ):
            try:
                t = time()
                # sending current time to the backend database (for the flight board to read and display)
                requests.post( config.simulation_time_url, json={"time": sm.simulation_minutes} )

                # getting airport environment (inputs)
                env = airport_io.update_environment( sm )
                file_writing.send_environment( sm, env )

                # getting current state to determine which check(s) should be done (to avoid doing all the checks so we can save time)
                current_state = sm.current_state.name

                # every 10 loops we call delay flights which delays the necessary flights on its own
                if (sm.loop_num % config.delay_checker_frequency == 9):
                    flight_delay_aux.delay_flights( sm )

                # states 0 - 2, and 23 ( over-the-sea states uneffected on airport conditions ) will always transition to next state after their associated time condition is met
                if (current_state in ["state_zero", "state_one", "state_two", "state_twenty_three"]):
                    sm.send_event("clear")
                
                # states 3 - 6 (normal path over the sea) and 25 - 28 (holding pattern) need the airport to have the "can-land" condition satisfied in order to transition
                elif (current_state in ["state_three", "state_four", "state_five", "state_six", "state_twenty_five"]):
                    if flight_delay_aux.check_for_cancellation( sm , current_state ):
                        sm.send_event("delayed-beyond-limit")
                        print("canceled flight")
                    elif (event_checkers.check_can_land(sm.day, env['beacon_light'], env['approach_lights'], env['RW6L_lights'], env['gate_open'])):
                        sm.send_event("clear")
                    else:
                        sm.send_event("holding")
                
                # states 7 and 8 (landing and pre-fuel landing-strip states) need the airport to have the "can-advance-runway" condition satisfied in order to transition
                elif (current_state in ["state_seven", "state_eight"]):
                    if flight_delay_aux.check_for_cancellation( sm , current_state ):
                        sm.send_event("delayed-beyond-limit")
                    elif (event_checkers.check_can_advance_runway(sm.day, env['RW6L_lights'], env['gate_open'])):
                        sm.send_event("clear")
                
                # state 9 (fuel state) needs the airport to have the "can-fuel" condition satisfied in order to transition
                elif (current_state == "state_nine"):
                    if flight_delay_aux.check_for_cancellation( sm , current_state ):
                        sm.send_event("delayed-beyond-limit")
                    elif (event_checkers.check_can_fuel(sm.day, env['RW6L_lights'], env['fuel_depot_light'], env['gate_open'] )):
                        sm.send_event("clear")

                # states 10, 11 and 16 - 19 (taxiway states) need the airport to have the "can-advance-runway" (arguments adjusted for taxiway) condition satisfied in order to transition
                elif (current_state in ["state_ten", "state_eleven", "state_sixteen", "state_seventeen", "state_eighteen", "state_nineteen"]):
                    if flight_delay_aux.check_for_cancellation( sm , current_state ):
                        sm.send_event("delayed-beyond-limit")
                    elif (event_checkers.check_can_advance_runway( sm.day, env['taxiway_lights'], env['gate_open'] )):
                        sm.send_event("clear")

                # states 12 - 15 (at the ramp) needs the airport to have the "can_advance_ramp" conditions satisfied
                elif (current_state in ["state_twelve", "state_thirteen", "state_fourteen", "state_fifteen"]):
                    if flight_delay_aux.check_for_cancellation( sm , current_state ):
                        sm.send_event("delayed-beyond-limit")
                    elif (event_checkers.check_can_advance_ramp( env['gate_open'] )):
                        sm.send_event("clear")

                # states 20 - 22 (runway states)
                elif (current_state in ["state_twenty", "state_twenty_one", "state_twenty_two"]):
                    if flight_delay_aux.check_for_cancellation( sm , current_state ):
                        sm.send_event("delayed-beyond-limit")
                    elif (event_checkers.check_can_advance_runway( sm.day, env['RW6R_lights'], env['gate_open'] )):
                        sm.send_event("clear")

                # state 24 (final over-the-sea departed state) will always transition when its associated time condition is met
                elif (current_state == "state_twenty_four"):
                    # update flight delays - the remaining delay loops that were ignored because they were less than 10
                    if sm.send_event("clear"):
                        flight_delay_aux.delay_flights( sm )

                
                # sending the environment and relevant flight info to an output file (for the display driver to read and display)
                sleep(max(0, 1 - (time() - t))) # this is for the airplane animation to time up nicely in the display
                file_writing.send_environment( sm, env )

                # loop maintainence
                sm.loop_num += 1 # updating loop number (necessary for state transition logic)
                sm.simulation_minutes = (sm.simulation_minutes + sm.minutes_per_loop) # updating the sim time in minutes
                print(sm.current_state.name)
                sleep(max(0, 1.1 - (time() - t)))

            except Exception as e:
                print(e)
                pass # in case a reading error happens just continue

        # after COMPETITION time is up - send specially formatted environment and relevant flight info to the output file so the display driver knows it's time to display results
        file_writing.final_send_environment( sm, airport_io.update_environment( sm ) )
        airport_io.handle_exit( sm )

    except KeyboardInterrupt:
        airport_io.handle_exit( sm )

###############################################################################################################################################################################


# Driver

if __name__ == "__main__" :

    # determining whether its demo or competition mode from command line args
    mode = None

    if len( sys.argv ) == 1:
        mode = 'demo'
    elif len( sys.argv ) == 2:
        mode = 'competition'

    # validating configurations
    config_validator.run_all_validations( )

    # making sure the departure times align with the arrival times
    setup_aux.sync_departure_times( mode )

    # setting up the database
    setup_aux.reset_airplane_database( )

    # getting the airplanes
    flight_list = setup_aux.get_airplane_id_list( )

    state_machine = setup_aux.initialize_statemachine( mode, flight_list, airport_io.create_alcms_client(), airport_io.create_fuel_client(), airport_io.create_gate_client() )
    
    # run the loop associated with the mode
    if mode == 'demo':
        run_demo( state_machine )

    elif mode == 'competition':
        run_competition( state_machine )