// getting express
const express = require('express')

const auth = require("../authentication/auth");

// getting the request functions exported from airplaneControllers
const {
    createAirplane,
    getAirplanes,
    getAirplane,
    deleteAirplane,
    deleteManyAirplanes,
    updateAirplane,
    updateAirplanes
} = require('../controllers/airplaneControllers')

/*
creating router object
router is an organization of the routes of the api server
*/
const router = express.Router()

/*
route = '/api/airplanes/'
GET request that returns json objects of all of the airplanes in database
*/
router.get('/', auth, getAirplanes)

/*
route = '/api/airplanes/{airplane arrivingFrom field}'
GET request that returns json object of airplane associated w/ id in database
*/
router.get('/:sourceAirport', getAirplane)

/*
route = '/api/airplanes/'
POST request that adds new airplane to database
*/
router.post('/', createAirplane)

/*
route = '/api/airplanes/{airplane id}'
DELETE request that deletes airplanes associted / id in database
*/
router.delete('/:id', deleteAirplane)

// Route for deleting all airplanes or multiple airplanes
router.delete('/', deleteManyAirplanes);

/*
route = '/api/airplanes/batch'
PATCH request that updates fields of airplanes associated w/ arrivingFrom field
*/
router.patch('/batch', updateAirplanes);

/*
route = '/api/airplanes/<sourceAirport>'
PATCH request that updates fields of airplane associated w/ sourceAirport field
*/
router.patch('/:sourceAirport', updateAirplane)

// exporting the router with all the routes/requests
module.exports = router