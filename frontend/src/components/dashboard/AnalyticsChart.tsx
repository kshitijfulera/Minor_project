"use client"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts"

export default function AnalyticsChart({ data }: any) {

  if (!data || data.length === 0) {
    return <p>No data for chart</p>
  }

  const chartData = data.map((item: any, index: number) => ({
    name: item.filename || `Level ${index + 1}`,
    difficulty: item.difficulty_score || 0
  }))

  return (
    <div className="bg-white p-6 rounded-xl shadow mb-8">

      <h2 className="text-xl font-semibold mb-4">
        Difficulty Trend
      </h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="difficulty"
            stroke="#3b82f6"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>

    </div>
  )
}