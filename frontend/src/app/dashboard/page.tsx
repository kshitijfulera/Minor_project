"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "../../components/layout/DashboardLayout"
import UploadSection from "../../components/sections/UploadSection"
import AnalyticsChart from "../../components/dashboard/AnalyticsChart"
import History from "@/components/dashboard/History"

export default function DashboardPage() {

  // Always array
  const [levels, setLevels] = useState<any[]>([])

  const [stats, setStats] = useState({
    total: 0,
    avgDifficulty: 0
  })

  // Fetch safely
  const fetchLevels = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/levels")
      const json = await res.json()

      // ensure array
      const safeData = Array.isArray(json.data) ? json.data : []
      setLevels(safeData)

    } catch (err) {
      console.error("Fetch error:", err)
      setLevels([]) // fallback
    }
  }

  useEffect(() => {
    fetchLevels()
  }, [])

  // Compute stats safely
  useEffect(() => {
    if (!Array.isArray(levels) || levels.length === 0) {
      setStats({ total: 0, avgDifficulty: 0 })
      return
    }

    const valid = levels.filter(
      (l) => typeof l?.difficulty_score === "number"
    )

    if (valid.length === 0) {
      setStats({ total: 0, avgDifficulty: 0 })
      return
    }

    const avg =
      valid.reduce((a, b) => a + b.difficulty_score, 0) /
      valid.length

    setStats({
      total: valid.length,
      avgDifficulty: avg
    })

  }, [levels])

  return (
    <DashboardLayout>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-6 mb-8">

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-slate-500">Total Uploads</p>
          <h3 className="text-3xl font-bold text-indigo-600">
            {stats.total}
          </h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-slate-500">Avg Difficulty</p>
          <h3 className="text-3xl font-bold text-indigo-600">
            {stats.avgDifficulty.toFixed(2)}
          </h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-slate-500">System Status</p>
          <h3 className="text-3xl font-bold text-green-500">
            Active
          </h3>
        </div>

      </div>

      <UploadSection refreshData={fetchLevels} />

      <History data={levels} />

      <AnalyticsChart data={levels} />

    </DashboardLayout>
  )
}