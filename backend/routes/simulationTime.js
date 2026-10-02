const express = require('express');
const router = express.Router();

let simulationTime = 0;

// Route to simulation time
router.get('/', (req, res) => {
    if (simulationTime === undefined || simulationTime === null) {
        return res.status(404).json({ message: 'Simulation time not set' });
    }
    res.status(200).json({ simulationTime });
});

router.post('/', (req, res) => {
    const { time } = req.body;

    // Error checking
    if (time === undefined || time === null) {
        return res.status(400).json({ message: 'Time is required' });
    }

    simulationTime = time; // Update simulation time
    res.status(200).json({ message: 'Simulation time updated successfully', simulationTime });
});

module.exports = router;