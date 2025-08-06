import { useEffect } from 'react'
import { useAirplanesContext } from "../hooks/useAirplanesContext"
import { useSimulationTimeContext } from "../hooks/simulationTimeContext";
import '../index.css'

// components
import AirplaneDetails from '../components/AirplaneDetails'

/*
function that creates the home page

fetches airplane data using the backend API
displays the data to the home page
*/


const Home = () => {

    // getting all airplanes and dispatch from the context
    const {airplanes, dispatch} = useAirplanesContext()

    const { simulationTime, dispatch: simulationDispatch } = useSimulationTimeContext();

    // gets all airplanes using api
    const fetchAirplanes = async () => {

      const response = await fetch('/api/airplanes/', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
              'x-auth-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik1heCIsInJvbGVzIjoiQWRtaW4iLCJpYXQiOjE3MTkzMzQ3Njl9.V7lqhmQZ996Vs3jNxLwjD01inR8aiuy8hpI-gm9IiFE'
        }
      });
        
        // getting json array of airplane objects
        const json = await response.json()

        //if the airplane data is returned with no errors
        if (response.ok) {
            
            dispatch({type: 'SET_AIRPLANES', payload: json})
        }
    }

    // Fetch simulation time every second
    const fetchSimulationTime = async () => {
        const response = await fetch('/simulationtime', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const json = await response.json();

        let input_minutes = json.simulationTime; // Simulation time in minutes
        
        const adjustedMinutes = input_minutes % 1440; // Wrap around 24-hour format (1440 minutes in a day)

        // Calculate the hour and 12-hour-period (AM/PM)
        const hours = Math.floor(adjustedMinutes / 60);
        const period = hours >= 12 ? "PM" : "AM";
        // 12-hour format
        const twelveHourFormat = hours % 12 || 12; // (0 becomes 12)
        // minutes
        const minutes = Math.floor(adjustedMinutes % 60);
        // Format the minutes with a leading zero if necessary
        const formattedMinutes = minutes.toString().padStart(2, "0");
        // formatted time
        let time = `${twelveHourFormat}:${formattedMinutes}\u200A${period}`;

        
        if (response.ok) {
            simulationDispatch({ type: 'SET_SIMULATION_TIME', payload: time });
        }
    };

    useEffect(() => {

        // getting array of all airplane objects using backend api and putting it in the context
        const intervalId = setInterval(fetchAirplanes, 1000);
        const simulationTimeInterval = setInterval(fetchSimulationTime, 1000);
        return () => {
          clearInterval(intervalId);
          clearInterval(simulationTimeInterval);
      };
    })
    
    return (
      <div className='home'>
        <div className='container'>
          <div className='header'>
            <div className='image-container'>
              <img src='/ta3.png' alt='Airplane' />
            </div>
            <div className='heading-text-container'>
              <h1 className='main-heading'>Arrivals & Departures</h1>
              <h2 className='sub-heading'>(HNL) Honolulu International</h2>
            </div>
            <div className='time-container'>
              <h2 className='time'>{simulationTime}</h2>
            </div>
          </div>
          <div className='flight-table-container'>
            <table className='flight-table'>
              <thead>
                <tr>
                  <th>Flying From</th>
                  <th>Flight</th>
                  <th>ETA</th>
                  <th>Gate</th>
                  <th><span>Status&nbsp;&nbsp;</span></th>
                  <th> </th> {/* Empty column for spacing */}
                  <th>Flying To</th>
                  <th>Flight</th>
                  <th>ETD</th>
                  <th>Gate</th>
                  <th><span>Status&nbsp;&nbsp;</span></th>
                </tr>
              </thead>
              <tbody>
                {airplanes && airplanes.map((airplane) => (
                  <AirplaneDetails key={airplane._id} airplane={airplane} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
}

export default Home