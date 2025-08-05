import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { AirplanesContextProvider } from './context/AirplaneContext'
import { SimulationTimeProvider } from './hooks/simulationTimeContext'; // Import the provider

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AirplanesContextProvider>
    <SimulationTimeProvider>
        <App />
      </SimulationTimeProvider>
    </AirplanesContextProvider>
  </React.StrictMode>
);
