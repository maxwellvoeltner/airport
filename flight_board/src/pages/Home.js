import { useAirplanesContext } from "../context/AirplaneContext"
import { useSimulationTimeContext } from "../context/SimulationTimeContext";
import '../index.css'

import AirplaneDetails from '../components/AirplaneDetails'

const Home = () => {

    // getting all airplanes and dispatch from the context
    const airplanes = useAirplanesContext();
    const simulationTime = useSimulationTimeContext();
    
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