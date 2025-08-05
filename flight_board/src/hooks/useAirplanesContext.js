import { AirplaneContext } from '../context/AirplaneContext'
import { useContext } from 'react'

export const useAirplanesContext = () => {
    const context = useContext(AirplaneContext)

    if (!context) {
        throw Error('useAirplanesContext must be used inside a AirplaneContextProvider')
    }

    return context
}