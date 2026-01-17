// getting the airplane model
const Airplane = require('../models/airplaneModel')
// getting mongoose
const mongoose = require('mongoose')

const getAirplanes = async (req, res) => {

    // getting all airplanes in database in ascending order of when they were created
    const airplanes = await Airplane.find({}).sort({createdAt: -1})

    /*
    responding w/:
    status 200 = everything's good
    json(airplanes) = json objects of all airplanes in database
    */
    res.status(200).json(airplanes)
}

/*
associated w/ request: GET and route: '/api/airplanes/{sourceAirport}'
returns json object of airplane associated w/ source airport in database
*/
const getAirplane = async (req, res) => {
    // Extracting "sourceAirport" from request parameters
    const { sourceAirport } = req.params;

    try {
        // Finding the airplane by the "sourceAirport" field
        const airplane = await Airplane.findOne({ "sourceAirport": sourceAirport });

        if (!airplane) {
            return res.status(404).json({ error: "No airplane found with the specified sourceAirport value" });
        }
        
        res.status(200).json(airplane);
    } catch (error) {
        // Handle any errors during the database query
        res.status(500).json({ error: "Server error while fetching airplane" });
    }
};


const createAirplane = async (req, res) => {

    // getting the source airport, arrival flight, arrival time, arrival status, departure flight, departure time, departure status, and gate from body of request
    const {sourceAirport, arrivalFlight, arrivalTime, arrivalStatus, departureFlight, departureTime, departureStatus, gate} = req.body

    let emptyFields = []

    // if source airport is null (no source airport location was given)
    if (!sourceAirport) {

        // add 'sourceAirport' to empty fields
        emptyFields.push('sourceAirport')
    }

    // if the arrival flight is null (no arrival flight was given)
    if (!arrivalFlight) {

        // add 'arrivalFlight' to empty fields
        emptyFields.push('arrivalFlight')
    }

    // if the arrival time is null (no arrival time was given)
    if (arrivalTime == null) {
        
        // add 'arrivalTime' to empty fields
        emptyFields.push('arrivalTime')
    }

    // if arrivalStatus to is null (no arrivalStatus time was given)
    if (!arrivalStatus) {

        // add 'arrivalStatus' to empty fields
        emptyFields.push('arrivalStatus')
    }

    // if the departure flight is null (no departure flight number was given)
    if (!departureFlight) {

        // add 'departureFlight' to empty fields
        emptyFields.push('departureFlight')
    }

    // if the departure time is null (no departure time was given)
    if (departureTime == null) {

        // add 'departureTime' to empty fields
        emptyFields.push('departureTime')
    }

    // if departure status to is null (no departure status was given)
    if (!departureStatus) {

        // add 'departure status' to empty fields
        emptyFields.push('departureStatus')
    }

    // if gate to is null (no gate was given)
    if (!gate) {

        // add 'gate' to empty fields
        emptyFields.push('gate')
    }

    // if there is at least 1 empty field
    if (emptyFields.length > 0) {

        // return because this function is over if this situation happens
        return res.status(400).json({ error: 'Please fill in all fields', emptyFields })
    }

    // adding airplane to database
    try {

        // creating airplane json object with field values from params of requests
        const airplane = await Airplane.create({sourceAirport, arrivalFlight, arrivalTime, arrivalStatus, departureFlight, departureTime, departureStatus, gate})

        res.status(200).json(airplane)
    
    //error case
    } catch (error) {

        res.status(400).json({error: error.message})
    }
}

const deleteAirplane = async (req, res) => {

    // getting id from params of request
    const { id } = req.params

    // if the id is not a valid MongoDB id
    if (!mongoose.Types.ObjectId.isValid(id)) {

        // return because this function is over if this situation happens
        return res.status(404).json({error: 'No such airplane'})
    }

    // getting airplane and deleting airplane entry from database
    const airplane = await Airplane.findOneAndDelete({_id: id})

    // if airplane is null (no airplane in database w/ given id)
    if (!airplane) {

        // return because this function is over if this situation happens
        return res.status(404).json({error: "No such airplane"})
    }

    res.status(200).json(airplane)
 }

// delete all airplanes
const deleteManyAirplanes = async (req, res) => {
    try {
        // If you want to delete all airplanes, you can use an empty filter
        const result = await Airplane.deleteMany({});

        // If no airplanes were deleted, you can return a message
        if (result.deletedCount === 0) {
            return res.status(404).json({ error: 'No airplanes were deleted' });
        }

        // Respond with success
        res.status(200).json({ message: `${result.deletedCount} airplane(s) deleted` });
    } catch (err) {
        res.status(500).json({ error: 'Something went wrong' });
    }
};


//update a airplane
const updateAirplane = async (req, res) => {

    // getting source airport from params of request
    const { sourceAirport } = req.params

    const airplane = await Airplane.findOneAndUpdate({sourceAirport: sourceAirport}, {
        ...req.body
    })

    // if airplane is null (no airplane in database w/ given id)
    if (!airplane) {

        // return because this function is over if this situation happens
        return res.status(404).json({error: "No such airplane"})
    }

    res.status(200).json(airplane)
}

// update multiple airplanes using bulkWrite
const updateAirplanes = async (req, res) => {
    const updates = req.body; // should be an array of { sourceAirport, update }

    if (!Array.isArray(updates)) {
        return res.status(400).json({ error: "Expected an array of update objects" });
    }

    const operations = updates.map(({ sourceAirport, update }) => {
        if (!sourceAirport || !update) return null;

        return {
            updateOne: {
                filter: { sourceAirport },
                update: { $set: update }
            }
        };
    }).filter(Boolean); // remove any nulls

    if (operations.length === 0) {
        return res.status(400).json({ error: "No valid update operations provided" });
    }

    try {
        const result = await Airplane.bulkWrite(operations);
        res.status(200).json({ message: "Batch update complete", result });
    } catch (error) {
        console.error("Batch update error:", error);
        res.status(500).json({ error: "Batch update failed", details: error.message });
    }
};


// exporting the functions for the router to store with the associated requests/routes
module.exports = {
    getAirplanes,
    getAirplane,
    createAirplane,
    deleteAirplane,
    deleteManyAirplanes,
    updateAirplane,
    updateAirplanes

}
