"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "../../components/layout/DashboardLayout"
import UploadSection from "../../components/sections/UploadSection"

export default function DashboardPage() {

  // ✅ Persistent stats (localStorage)
  const [stats, setStats] = useState(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("stats")
      return saved
        ? JSON.parse(saved)
        : { total: 0, avgDifficulty: 0 }
    }
    return { total: 0, avgDifficulty: 0 }
  })

  // ✅ Save to localStorage whenever stats change
  useEffect(() => {
    localStorage.setItem("stats", JSON.stringify(stats))
  }, [stats])

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

      {/* 📤 Upload Section (passes setStats) */}
      <UploadSection setStats={setStats} />

    </DashboardLayout>
  )
}