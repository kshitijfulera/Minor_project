"use client"

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js"

import { Bar } from "react-chartjs-2"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default function DifficultyChart({ features }: any) {

  const data = {
    labels: ["Enemies", "Spawn Rate", "Rewards", "Checkpoints"],
    datasets: [
      {
        label: "Level Features",
        data: [
          features.enemy_count,
          features.spawn_rate,
          features.rewards,
          features.checkpoints
        ],
      },
    ],
  }

  return <Bar data={data} />
}