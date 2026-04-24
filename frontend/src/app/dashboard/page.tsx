"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "../../components/layout/DashboardLayout"
import UploadSection from "../../components/sections/UploadSection"
import AnalyticsChart from "../../components/dashboard/AnalyticsChart"
import History from "../../components/dashboard/History"

export default function DashboardPage() {

  // 📦 Store all levels from DB
  const [levels, setLevels] = useState<any[]>([])

  // 📊 Stats (derived from DB, NOT localStorage anymore)
  const [stats, setStats] = useState({
    total: 0,
    avgDifficulty: 0
  })

  // 🚀 Fetch data from backend
  const fetchLevels = () => {
    fetch("http://127.0.0.1:8000/levels")
      .then(res => res.json())
      .then(res => {
        setLevels(res.data)
      })
      .catch(err => console.error("Fetch error:", err))
  }

  // 🔁 Load data on page load
  useEffect(() => {
    fetchLevels()
  }, [])

  // 📊 Compute stats from DB data
  useEffect(() => {
    if (levels.length > 0) {
      const difficulties = levels.map(l => l.difficulty_score)

      const avg =
        difficulties.reduce((a, b) => a + b, 0) /
        difficulties.length

      setStats({
        total: levels.length,
        avgDifficulty: avg
      })
    } else {
      setStats({
        total: 0,
        avgDifficulty: 0
      })
    }
  }, [levels])

  return (
    <DashboardLayout>

      {/* 🔴 Reset Button */}
      <button
        onClick={() => setStats({ total: 0, avgDifficulty: 0 })}
        className="mb-6 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
      >
        Reset Stats
      </button>

      {/* 📊 Stats Cards */}
      <div className="grid grid-cols-3 gap-6 mb-8">

        <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
          <p className="text-slate-500">Total Uploads</p>
          <h3 className="text-3xl font-bold text-indigo-600">
            {stats.total}
          </h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
          <p className="text-slate-500">Avg Difficulty</p>
          <h3 className="text-3xl font-bold text-indigo-600">
            {stats.avgDifficulty.toFixed(2)}
          </h3>
        </div>

        <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
          <p className="text-slate-500">System Status</p>
          <h3 className="text-3xl font-bold text-green-500">
            Active
          </h3>
        </div>

      </div>

      {/* 📤 Upload Section */}
      <UploadSection
        setStats={setStats}
        refreshData={fetchLevels}   // 🔥 refresh after upload
      />

      {/* 📜 History */}
      <History data={levels} />

      {/* 📈 Analytics Chart */}
      <AnalyticsChart data={levels} />

    </DashboardLayout>
  )
}