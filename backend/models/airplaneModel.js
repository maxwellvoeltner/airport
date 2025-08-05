// getting mongoose
const mongoose = require('mongoose')

/*
It defines the structure of documents within a MongoDB collection
A schema in Mongoose maps directly to a MongoDB collection
and defines the shape of the documents within that collection.
*/
const Schema = mongoose.Schema

/*
creating structure for all airplane "documents" in the MongoDB
first argument: schema object
*/
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