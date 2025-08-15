// AirplaneContext.js
import { createContext, useContext, useState, useEffect } from 'react';

export const AirplaneContext = createContext();

export const AirplanesContextProvider = ({ children }) => {
  const [airplanes, setAirplanes] = useState(null);

  useEffect(() => {
    const fetchAirplanes = async () => {
      try {
        const response = await fetch('/api/airplanes/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'x-auth-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik1heCIsInJvbGVzIjoiQWRtaW4iLCJpYXQiOjE3MTkzMzQ3Njl9.V7lqhmQZ996Vs3jNxLwjD01inR8aiuy8hpI-gm9IiFE'
          },
        });

        if (!response.ok) return;

        const json = await response.json();
        setAirplanes(json);
      } catch (err) {
        console.error('Failed to fetch airplanes:', err);
      }
    };

    const interval = setInterval(fetchAirplanes, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AirplaneContext.Provider value={airplanes}>
      {children}
    </AirplaneContext.Provider>
  );
};


export const useAirplanesContext = () => {
  const context = useContext(AirplaneContext);
  if (context === undefined) {
    throw new Error('useAirplanesContext must be used within an AirplanesContextProvider');
  }
  return context;
};