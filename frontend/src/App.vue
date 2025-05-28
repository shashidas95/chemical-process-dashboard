<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import LineChart from './components/LineChart.vue' // Import our new component

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL // Access env variable
const chartData = ref({
  labels: [],
  datasets: [],
})
const errorMessage = ref('')

// Define process parameters we want to display (must match CSV headers)
const processParameters = [
  {
    key: 'Temperature',
    label: 'Temperature (°C)',
    color: 'rgba(255, 99, 132, 1)',
  },
  { key: 'Pressure', label: 'Pressure (Bar)', color: 'rgba(54, 162, 235, 1)' },
  {
    key: 'Flow_Rate',
    label: 'Flow Rate (L/min)',
    color: 'rgba(255, 206, 86, 1)',
  },
  { key: 'pH_Value', label: 'pH Value', color: 'rgba(75, 192, 192, 1)' },
  {
    key: 'Concentration',
    label: 'Concentration (mol/L)',
    color: 'rgba(153, 102, 255, 1)',
  },
]

const fetchData = async () => {
  try {
    errorMessage.value = '' // Clear previous errors
    // Fetch 500 latest data points for a good initial view
    const response = await axios.get(`${API_BASE_URL}/api/data/latest/500`)
    console.log('Axios response:', response) // <-- ADD THIS LINE
    const data = response.data
    console.log('Data received from API:', data) // <-- ADD THIS LINE

    if (!data || data.length === 0) {
      errorMessage.value = 'No data received from API.'
      chartData.value.labels = []
      chartData.value.datasets = []
      return
    }

    // Extract labels (timestamps)
    const labels = data.map((row) => new Date(row.timestamp).toISOString()) // Use ISO string for consistent parsing by Chart.js

    // Prepare datasets for each parameter
    const datasets = processParameters.map((param) => ({
      label: param.label,
      data: data.map((row) => row[param.key]),
      borderColor: param.color,
      backgroundColor: param.color.replace('1)', '0.2)'), // Lighter background for area under line
      borderWidth: 2,
      pointRadius: 0, // No points for cleaner line charts
      fill: false, // Don't fill area under the line by default
      tension: 0.1, // Smooth out the lines
    }))

    chartData.value = { labels, datasets }
  } catch (error) {
    console.error('Error fetching data:', error)
    errorMessage.value = `Failed to fetch data: ${error.message}. Please ensure the backend server is running on ${API_BASE_URL}.`
    chartData.value.labels = []
    chartData.value.datasets = []
  }
}

// Fetch data when the component is mounted
onMounted(() => {
  fetchData()
  // Optional: Set up interval for refreshing data
  // setInterval(fetchData, 10000); // Refresh every 10 seconds (adjust as needed)
})
</script>

<template>
  <div id="app" class="p-8">
    <h1 class="text-3xl font-bold mb-8 text-center">
      Chemical Process Monitoring Dashboard
    </h1>

    <div
      v-if="errorMessage"
      class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
      role="alert"
    >
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline ml-2">{{ errorMessage }}</span>
    </div>

    <div v-if="chartData.datasets.length > 0" class="chart-container">
      <LineChart :chartData="chartData" />
    </div>
    <div v-else-if="!errorMessage" class="text-center text-gray-500">
      Loading data...
    </div>
  </div>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 1200px;
  margin: 0 auto;
}
.text-center {
  text-align: center;
}
.text-3xl {
  font-size: 1.875rem; /* 30px */
}
.font-bold {
  font-weight: 700;
}
.mb-8 {
  margin-bottom: 2rem; /* 32px */
}
.p-8 {
  padding: 2rem;
}

/* Basic styling for error message */
.bg-red-100 {
  background-color: #fee2e2;
}
.border-red-400 {
  border-color: #fca5a5;
}
.text-red-700 {
  color: #b91c1c;
}
.rounded {
  border-radius: 0.25rem;
}
.relative {
  position: relative;
}
.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}
.py-3 {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.mb-4 {
  margin-bottom: 1rem;
}
.block {
  display: block;
}
.sm\:inline {
  display: inline;
}
.ml-2 {
  margin-left: 0.5rem;
}

/* Basic styling for chart container to give it some height */
.chart-container {
  position: relative;
  height: 400px; /* Adjust height as needed */
  width: 100%;
  background-color: #f8f8f8;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
