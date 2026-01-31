import React from "react";
import { Bar, Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
);

const Charts = ({ dataset }) => {
  if (!dataset) return null;

  const equipmentTypes = dataset.summary_data.equipment_types;

  // Bar chart for equipment type distribution
  const typeChartData = {
    labels: Object.keys(equipmentTypes),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(equipmentTypes),
        backgroundColor: "rgba(102, 126, 234, 0.6)",
        borderColor: "rgba(102, 126, 234, 1)",
        borderWidth: 1,
      },
    ],
  };

  // Pie chart for equipment type proportion
  const pieChartData = {
    labels: Object.keys(equipmentTypes),
    datasets: [
      {
        data: Object.values(equipmentTypes),
        backgroundColor: [
          "rgba(102, 126, 234, 0.6)",
          "rgba(118, 75, 162, 0.6)",
          "rgba(66, 153, 225, 0.6)",
          "rgba(72, 187, 120, 0.6)",
          "rgba(245, 101, 101, 0.6)",
          "rgba(246, 173, 85, 0.6)",
        ],
        borderColor: [
          "rgba(102, 126, 234, 1)",
          "rgba(118, 75, 162, 1)",
          "rgba(66, 153, 225, 1)",
          "rgba(72, 187, 120, 1)",
          "rgba(245, 101, 101, 1)",
          "rgba(246, 173, 85, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  // Line chart for parameter ranges
  const paramChartData = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
      {
        label: "Minimum",
        data: [
          dataset.summary_data.ranges.flowrate.min,
          dataset.summary_data.ranges.pressure.min,
          dataset.summary_data.ranges.temperature.min,
        ],
        borderColor: "rgb(245, 101, 101)",
        backgroundColor: "rgba(245, 101, 101, 0.5)",
        borderWidth: 2,
        tension: 0.4,
      },
      {
        label: "Maximum",
        data: [
          dataset.summary_data.ranges.flowrate.max,
          dataset.summary_data.ranges.pressure.max,
          dataset.summary_data.ranges.temperature.max,
        ],
        borderColor: "rgb(72, 187, 120)",
        backgroundColor: "rgba(72, 187, 120, 0.5)",
        borderWidth: 2,
        tension: 0.4,
      },
      {
        label: "Average",
        data: [
          dataset.summary_data.averages.flowrate,
          dataset.summary_data.averages.pressure,
          dataset.summary_data.averages.temperature,
        ],
        borderColor: "rgb(102, 126, 234)",
        backgroundColor: "rgba(102, 126, 234, 0.5)",
        borderWidth: 2,
        tension: 0.4,
        borderDash: [5, 5],
      },
    ],
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: false,
      },
    },
  };

  const pieOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "right",
      },
    },
  };

  const lineOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
  };

  return (
    <div className="charts-container">
      <div className="chart">
        <h3>📊 Equipment Type Distribution</h3>
        <Bar data={typeChartData} options={barOptions} />
      </div>
      <div className="chart">
        <h3>🥧 Equipment Type Proportion</h3>
        <Pie data={pieChartData} options={pieOptions} />
      </div>
      <div className="chart" style={{ gridColumn: "span 2" }}>
        <h3>📈 Parameter Analysis</h3>
        <Line data={paramChartData} options={lineOptions} />
      </div>
    </div>
  );
};

export default Charts;
