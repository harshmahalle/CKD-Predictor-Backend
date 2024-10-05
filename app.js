const express = require('express');
const connectDB = require('./config/db');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
const ckdRoutes = require('./routes/ckdRoutes');
const cors = require('cors'); 

dotenv.config();

// Connect to MongoDB
connectDB();

const app = express();

// Middleware
app.use(bodyParser.json());

// Enable CORS to allow requests from frontend
app.use(cors());

// Routes
app.use('/api/ckd', ckdRoutes);

// Root Endpoint
app.get('/', (req, res) => {
  res.send('CKD Detection API is running');
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

