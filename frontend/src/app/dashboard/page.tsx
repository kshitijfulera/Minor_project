"use client"

import { useEffect, useState } from "react"
import UploadSection from "../../components/sections/UploadSection"
import History from "../../components/dashboard/History"
import AnalyticsChart from "../../components/dashboard/AnalyticsChart"

export default function DashboardPage() {
  const [levels, setLevels] = useState<any[]>([])
  const [stats, setStats] = useState({
    total: 0,
    avgDifficulty: 0
  })

  // 🔄 Fetch all levels from backend
  const refreshData = async () => {
    try {
      const res = await fetch("http://localhost:8000/levels")
      const data = await res.json()

      const list = data?.data || []
      setLevels(list)

      // 📊 recompute stats
      if (list.length > 0) {
        const diffs = list.map((l: any) => l.difficulty_score || 0)
        const avg =
          diffs.reduce((a: number, b: number) => a + b, 0) / diffs.length

        setStats({
          total: list.length,
          avgDifficulty: avg
        })
      } else {
        setStats({ total: 0, avgDifficulty: 0 })
      }
    } catch (err) {
      console.error("Failed to fetch levels:", err)
    }
  }

  // 📥 Load once on page mount
  useEffect(() => {
    refreshData()
  }, [])

  return (
    <div className="p-6">

      {/* 🔹 Stats */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">Total Uploads</p>
          <h3 className="text-3xl font-bold">{stats.total}</h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">Avg Difficulty</p>
          <h3 className="text-3xl font-bold">
            {stats.avgDifficulty.toFixed(2)}
          </h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">System Status</p>
          <h3 className="text-green-500 font-bold">Active</h3>
        </div>
      </div>

      {/* 🔹 Upload */}
      <UploadSection
        setStats={setStats}
        refreshData={refreshData}
      />

      {/* 🔹 Chart */}
      <AnalyticsChart data={levels} />

      {/* 🔹 History */}
      <History data={levels} />

    </div>
  )
}