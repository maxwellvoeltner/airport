// createContext() lets you make a new context to provide to components
import { createContext, useReducer } from 'react'

// creating and exporting the context
export const AirplaneContext = createContext()

// 
export const airplanesReducer = (state, action) => {
    switch (action.type) {
        case 'SET_AIRPLANES':
            return {
                airplanes: action.payload
            }
        case 'CREATE_AIRPLANE':
            return  {
                airplanes: [action.payload, ...state.airplanes]
            }
        case 'DELETE_AIRPLANE':

            return {
                airplanes: state.airplanes.filter((w) => w._id !== action.payload._id)
            }
        default:
            return state
    }
}

/*
provide the context to components
wraps application so every component can use it
returning a template

children is the app component that is wrapped by the
context provider

by returning children wrapped by the context provider,
it's returning/executing the root component
which is what renders the app
so its a refresh 
*/
export const AirplanesContextProvider = ({ children }) => {

    /*
    use reducer:
    argument 1) reducer function
    argument 2) array of airplanes called airplanes that is null to begin with (initial value for state)
    */
    const [state, dispatch] = useReducer(airplanesReducer, {
        airplanes: null
    })

    // dispatch({type: 'SET_AIRPLANES', payload: [{}, {}]})

    return (
        <AirplaneContext.Provider value={{...state, dispatch}}>
          { children }
        </AirplaneContext.Provider>
    )
}