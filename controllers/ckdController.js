const path = require('path');
const { spawn } = require('child_process');
const CKD = require('../models/CKDModel');

// Start the Python process once when the server starts
const pythonProcess = spawn('python', [path.join(__dirname, '..', 'scripts', 'predictor.py')]);

// Handle Python process errors
pythonProcess.stderr.on('data', (data) => {
  console.error(`Python stderr: ${data}`);
});

// Optional: Handle Python process exit
pythonProcess.on('close', (code) => {
  console.log(`Python process exited with code ${code}`);
});

// Function to send data to Python and receive the response
const sendPredictionRequest = (inputData) => {
  return new Promise((resolve, reject) => {
    // Listen for a single line of response
    const onData = (data) => {
      const response = data.toString();
      resolve(response);
      pythonProcess.stdout.off('data', onData); 
    };

    pythonProcess.stdout.on('data', onData);

    // Send the input data as JSON string followed by a newline
    pythonProcess.stdin.write(JSON.stringify(inputData) + '\n');
  });
};

exports.predictCKD = async (req, res) => {
  const { sg, al, sc, hemo, pcv, htn } = req.body;

  console.log('Received prediction request with data:', req.body);

  try {
    const input = { sg, al, sc, hemo, pcv, htn };
    const predictionResponse = await sendPredictionRequest(input);

    const prediction = JSON.parse(predictionResponse);

    if (prediction.error) {
      console.error('Prediction Error:', prediction.error);
      return res.status(500).json({ error: 'Error in ML model prediction: ' + prediction.error });
    }

    console.log('Parsed prediction:', prediction);

    // Save result to MongoDB
    const newCKD = new CKD({
      sg,
      al,
      sc,
      hemo,
      pcv,
      htn,
      classification: prediction.prediction,
    });

    const savedData = await newCKD.save();

    console.log('Saved prediction to MongoDB:', savedData);

    res.status(200).json({
      message: 'Prediction success',
      data: savedData,
      probability: prediction.probability,
    });
  } catch (error) {
    console.error('Error during prediction:', error);
    res.status(500).json({ error: 'Error in ML model prediction' });
  }
};



