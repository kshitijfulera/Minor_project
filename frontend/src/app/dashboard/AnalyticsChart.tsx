"use client"

import { Bar } from "react-chartjs-2"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default function AnalyticsChart({ data }: any) {
  const labels = data.map((d: any) => d.filename)

  const difficulty = data.map((d: any) => d.difficulty_score)

  const chartData = {
    labels,
    datasets: [
      {
        label: "Difficulty Score",
        data: difficulty
      }
    ]
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow mt-6">
      <h3 className="text-lg font-semibold mb-4">Difficulty Analysis</h3>
      <Bar data={chartData} />
    </div>
  )
}