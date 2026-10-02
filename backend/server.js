// for the .env file that stores environment variables (ex: PORT)
require('dotenv').config()

// getting express to connect code to server
const express = require('express')


const mongoose = require('mongoose')

const airplaneRoutes = require('./routes/airplanes')

const simulationTimeRoutes = require('./routes/simulationTime')

const app = express()

app.use(express.json())

/*
express function that has access to the request and response
logs the request to the console
next() goes to the next middleware function
*/
app.use((req, res, next) => {
    //console.log(req.path, req.method)
    next()
})

// giving expresss the router with the routes starting at '/api/airplanes'
app.use('/api/airplanes', airplaneRoutes)

app.use('/simulationtime', simulationTimeRoutes)


// establishing connection to MongoDB
mongoose.connect(process.env.LOCAL_MONGO_URI)
    .then(() => {
        // listen for requests
        // listen for requests
        app.listen(process.env.PORT, () => {
            console.log('connected to db & listening on port', process.env.PORT)
        })
    })
    .catch((error) => {
        console.log(error)
    })

