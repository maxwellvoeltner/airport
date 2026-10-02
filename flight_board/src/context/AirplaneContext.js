// AirplaneContext.js
import { createContext, useContext, useState, useEffect } from 'react';

/*
The channel itself, not the data.
what useContext reads from (to get data out)
.Provider (to put data in)
*/
export const AirplaneContext = createContext();

export const AirplanesContextProvider = ({ children }) => {
  /* useState()[0] => current state
     useState()[1] => function to update state */
  const [airplanes, setAirplanes] = useState(null);

  useEffect(() => {
    const fetchAirplanes = async () => {
      try {
        const response = await fetch('/api/airplanes/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'x-auth-token': ''
          }
        });

        if (!response.ok) return;

        const json = await response.json();
        /* Calling setAirplanes is how you tell React "re-run this component's function body, and this time, let airplanes equal this new value." */
        setAirplanes(json);
      } catch (err) {
        console.error('Failed to fetch airplanes:', err);
      }
    };

    // api call to the browser to run fetch airplanes every second
    const interval = setInterval(fetchAirplanes, 1000);
    // doesnt actually return - just runs when AirplanesContextProvider gets unmounted when the app closes
    return () => clearInterval(interval);
  }, []);

  /*
  JSX for the airplane context provider and the app inside it
  the children need to be in the JSX so they have access to the airplane context
  value 
  */
  return (
    <AirplaneContext.Provider value={airplanes}>
      {children}
    </AirplaneContext.Provider>
  );
};

// gets latest airplane data
export const useAirplanesContext = () => {
  const context = useContext(AirplaneContext);
  if (context === undefined) {
    throw new Error('useAirplanesContext must be used within an AirplanesContextProvider');
  }
  return context;
};