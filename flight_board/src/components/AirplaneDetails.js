function minutesToTime(minutes) {

  if (minutes === -1) {
    return "‒‒:‒‒"
  }

  const totalMinutes = Math.floor(minutes); // Round down to the nearest whole minute
  const hours = (Math.floor(totalMinutes / 60)) % 24;
  const mins = totalMinutes % 60;
  
  const hoursStr = String(hours).padStart(2, '0'); // two digits for hours
  const minsStr = String(mins).padStart(2, '0');   // two digits for minutes
  
  return `${hoursStr}:${minsStr}`;
}

const AirplaneDetails = ({ airplane }) => {

  const getStatusDot = (status) => {
    let color;
  
    switch (status) {
      case "Scheduled":
      case "Arrived":
      case "Departed":
        color = '#A8E04D';
        break;
      case "En Route":
        color = '#036cc8ff';
        break;
      case "Holding":
        color = '#FF8C00';
        break;
      case "On Approach":
        color = '#0070d1ff';
        break;
      case "Delayed":
      case "Cancelled":
        color = '#FF0000';
        break;
      case "Taxiing":
        color = '#800080';
        break;
      case "On Runway":
        color = '#0000FF';
        break;
      case "Boarding":
      case "Check-In":
        color = '#FF7F00';
        break;
      default:
        color = '#FFFFFF';
    }

    if (/^Rerouted \(.+\)$/.test(status)) { // regex isn't supported in switch statements so we gotta check for rerouted out here since we dont know the Airport ahead of time
      color = '#FF0000';
    }
  
    return <span style={{ color: color, fontSize: '2.4vh' }}>&nbsp;&nbsp;⬤</span>;
  };  

    return (
      <tr>
        <td>{airplane.sourceAirport}</td>
        <td>{airplane.arrivalFlight}</td>
        <td>{minutesToTime(airplane.arrivalTime)}</td>
        <td>{airplane.gate}</td>
        <td>{airplane.arrivalStatus}{getStatusDot(airplane.arrivalStatus)}</td>
        <td></td>
        <td>{airplane.sourceAirport}</td>
        <td>{airplane.departureFlight}</td>
        <td>{minutesToTime(airplane.departureTime)}</td>
        <td>{airplane.gate}</td>
        <td>{airplane.departureStatus}{getStatusDot(airplane.departureStatus)}</td>
      </tr>
    );
}

export default AirplaneDetails