// SimulationTimeContext.js
import { createContext, useContext, useState, useEffect } from 'react';

// Create the context
export const SimulationTimeContext = createContext();

// Provider component
export const SimulationTimeProvider = ({ children }) => {
  const [simulationTime, setSimulationTime] = useState(null);

  useEffect(() => {
    const fetchSimulationTime = async () => {
      try {
        const response = await fetch('/simulationtime', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) return;

        const json = await response.json();
        let input_minutes = json.simulationTime;
        if (input_minutes < 0) input_minutes += 1440;
        const adjustedMinutes = input_minutes % 1440;

        const hours = Math.floor(adjustedMinutes / 60);
        const period = hours >= 12 ? 'PM' : 'AM';
        const twelveHourFormat = hours % 12 || 12;
        const minutes = Math.floor(adjustedMinutes % 60);
        const formattedMinutes = minutes.toString().padStart(2, '0');
        const time = `${twelveHourFormat}:${formattedMinutes}\u200A${period}`;

        setSimulationTime(time);
      } catch (err) {
        console.error("Failed to fetch simulation time", err);
      }
    };

    const interval = setInterval(fetchSimulationTime, 1100);
    return () => clearInterval(interval);
  }, []);

  return (
    <SimulationTimeContext.Provider value={simulationTime}>
      {children}
    </SimulationTimeContext.Provider>
  );
};

// Custom hook
export const useSimulationTimeContext = () => useContext(SimulationTimeContext);