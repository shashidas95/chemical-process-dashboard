const express = require('express');
const cors = require('cors');
const fs = require('fs');
const csv = require('csv-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001; // API will run on port 3001

// --- Middleware ---
app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Enable JSON body parsing for requests (not strictly needed for GET, but good practice)

// --- Configuration ---
const DATA_FILE_PATH = path.join(__dirname, '..', 'data', 'process_data.csv'); // Path to our CSV file

// --- Helper Function to Read Data ---
async function readProcessData() {
 return new Promise((resolve, reject) => {
  const results = [];
  fs.createReadStream(DATA_FILE_PATH)
   .pipe(csv({ headers: true, skipEmptyLines: true }))
   .on('data', (data) => {
    // Convert string values to numbers where appropriate
    for (const key in data) {
     if (key !== 'timestamp' && !isNaN(data[key])) {
      data[key] = parseFloat(data[key]);
     }
    }
    results.push(data);
   })
   .on('end', () => {
    console.log('CSV file successfully processed.');
    resolve(results);
   })
   .on('error', (error) => {
    console.error('Error reading CSV file:', error);
    reject(error);
   });
 });
}

// --- API Endpoints ---

// Root route
app.get('/', (req, res) => {
 res.send('Chemical Process Dashboard API is running!');
});

// Endpoint to get all process data
app.get('/api/data', async (req, res) => {
 try {
  const data = await readProcessData();
  res.json(data);
 } catch (error) {
  console.error('Failed to retrieve process data:', error);
  res.status(500).json({ message: 'Error retrieving process data' });
 }
});

// Endpoint to get a specific number of latest data points
app.get('/api/data/latest/:count', async (req, res) => {
 const count = parseInt(req.params.count);
 if (isNaN(count) || count <= 0) {
  return res.status(400).json({ message: 'Invalid count parameter. Must be a positive integer.' });
 }

 try {
  const allData = await readProcessData();
  // Sort by timestamp in descending order and take the latest 'count'
  const latestData = allData
   .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
   .slice(0, count);
  res.json(latestData.reverse()); // Reverse to get oldest-to-newest for charts
 } catch (error) {
  console.error('Failed to retrieve latest process data:', error);
  res.status(500).json({ message: 'Error retrieving latest process data' });
 }
});


// --- Start Server ---
app.listen(PORT, () => {
 console.log(`Server running on port ${PORT}`);
 console.log(`Access API at http://localhost:${PORT}`);
});