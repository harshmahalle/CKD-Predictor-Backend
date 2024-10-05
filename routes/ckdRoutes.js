const express = require('express');
const router = express.Router();
const { predictCKD } = require('../controllers/ckdController');

router.post('/predict', predictCKD);

module.exports = router;
