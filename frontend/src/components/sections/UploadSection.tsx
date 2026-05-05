"use client"

import { useCallback, useState } from "react"
import toast from "react-hot-toast"

export default function UploadSection({
  setStats,
  refreshData
}: any) {

  const [loading, setLoading] = useState(false)

  const onUpload = useCallback(async (event: any) => {
  const files = event.target.files
  if (!files || files.length === 0) return

  try {
    setLoading(true)

    for (let file of files) {
      const formData = new FormData()
      formData.append("file", file)

      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData
      })

      const data = await res.json()

      if (!res.ok || data.error) {
        toast.error(`❌ Failed: ${file.name}`)
        continue
      }

      // ✅ Success toast
      toast.success(`✅ Uploaded: ${file.name}`)

      // update stats
      setStats((prev: any) => {
        const newTotal = prev.total + 1
        const newAvg =
          (prev.avgDifficulty * prev.total + data.difficulty_score) /
          newTotal

        return {
          total: newTotal,
          avgDifficulty: newAvg
        }
      })
    }

    // 🔄 Refresh dashboard
    await refreshData()

  } catch (err) {
    console.error(err)
    toast.error("🚨 Upload failed. Server not reachable.")
  } finally {
    setLoading(false)
  }

}, [setStats, refreshData])

  return (
    <div className="mb-6">

      {/* 📤 File input */}
      <input
        type="file"
        accept=".json"
        multiple
        onChange={onUpload}
        className="border p-2 rounded"
      />

      {/* ⏳ Loading */}
      {loading && (
        <div className="mt-3 flex items-center gap-2 text-blue-500 text-sm">
          <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
          Processing...
        </div>
      )}

    </div>
  )
}