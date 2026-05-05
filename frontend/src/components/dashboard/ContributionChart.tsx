"use client"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts"

export default function ContributionChart({ contributions }: any) {

  if (!contributions) return null

  const data = Object.entries(contributions).map(
    ([key, value]: any) => ({
      feature: key,
      value: Number(value)
    })
  )

  return (
    <div className="bg-white p-4 rounded-lg shadow mt-3">

      <h3 className="text-sm font-medium mb-2">
        Feature Impact
      </h3>

      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data}>
          <XAxis dataKey="feature" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#10b981" />
        </BarChart>
      </ResponsiveContainer>

    </div>
  )
}