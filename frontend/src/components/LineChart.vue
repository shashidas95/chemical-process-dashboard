<script setup>
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

// Define props for the component
const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            title: function(context) {
              // Format timestamp nicely
              const timestamp = context[0].label;
              return new Date(timestamp).toLocaleString();
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Time'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            callback: function(val, index) {
              // Display only specific ticks to avoid clutter
              // Example: show every 10th label
              return index % 10 === 0 ? new Date(this.getLabelForValue(val)).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
            }
          }
        },
        y: {
          title: {
            display: true,
            text: 'Value'
          }
        }
      }
    })
  }
});
</script>

<template>
  <Line :data="chartData" :options="chartOptions" />
</template>