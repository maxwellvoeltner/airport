import { createContext, useContext, useReducer } from 'react';

// Create the context for simulation time
export const SimulationTimeContext = createContext();

// Reducer function to manage simulation time state
export const simulationTimeReducer = (state, action) => {
    switch (action.type) {
        case 'SET_SIMULATION_TIME':
            return {
                simulationTime: action.payload
            };
        case 'UPDATE_SIMULATION_TIME':
            return {
                simulationTime: action.payload
            };
        default:
            return state;
    }
};

// Provider component to wrap around the app
export const SimulationTimeProvider = ({ children }) => {
    const [state, dispatch] = useReducer(simulationTimeReducer, {
        simulationTime: null // Default simulation time is null
    });

    return (
        <SimulationTimeContext.Provider value={{ ...state, dispatch }}>
            {children}
        </SimulationTimeContext.Provider>
    );
};

// Custom hook to use the simulation time context
export const useSimulationTimeContext = () => {
    return useContext(SimulationTimeContext);
};
