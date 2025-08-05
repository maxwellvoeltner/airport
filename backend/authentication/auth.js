// Import dependencies
require('dotenv').config()
const jwt = require("jsonwebtoken");

module.exports = (req, res, next) => {
    const token = req.header("x-auth-token");
    if (!token) return res.status(401).send({
        ok: false,
        error: "Access denied. No token provided"
    });

    try {
        const decoded = jwt.verify(token, process.env.JWTKey);
        req.user = decoded;
    } catch (error) {
        return res.status(401).send({
            ok: false,
            error: "Invalid Token"
        });
    }

    next();
}