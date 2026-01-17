// getting mongoose
const mongoose = require('mongoose')

const Schema = mongoose.Schema

const airplaneSchema = new Schema({

     // acronym of airport airplane is arriving from and departing to
     sourceAirport: {
        type: String,
        required: true,
        unique: true
    },

    // name of arriving flight
    arrivalFlight: {
        type: String,
        required: true
    },

    // arrival time: minutes past 12:00am
    arrivalTime: {
        type: Number,
        required: true
    },

     // status of arrival
     arrivalStatus: {
        type: String,
        required: true
    },

    // name of departing flight
    departureFlight: {
        type: String,
        required: true
    },

    // departure time: minutes past 12:00am
    departureTime: {
        type: Number,
        required: true
    },

    // status of departure
    departureStatus: {
        type: String,
        required: true
    },

    // name of gate airplane checks into
    gate: {
        type: String,
        required: true
    }
})

// exporting the airplane model

module.exports = mongoose.model('Airplane', airplaneSchema, 'cluster0')
