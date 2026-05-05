"use client"

import ContributionChart from "./ContributionChart"

export default function History({ data }: any) {

  if (!data || data.length === 0) {
    return (
      <p className="text-gray-500">
        No data yet. Upload a level to see results.
      </p>
    )
  }

  // 🎯 Confidence label + color
  const getConfidenceLabel = (c: number) => {
    if (c > 0.8) return { label: "High", color: "bg-green-500" }
    if (c > 0.6) return { label: "Medium", color: "bg-yellow-500" }
    return { label: "Low", color: "bg-red-500" }
  }

  // 🎯 Difficulty color
  const getDifficultyColor = (d: number) => {
    if (d > 0.7) return "text-red-500"
    if (d > 0.4) return "text-yellow-500"
    return "text-green-500"
  }

  return (
    <div className="space-y-5">

      {data.map((item: any, index: number) => {

        const difficulty = item.difficulty_score || 0
        const confidence = item.confidence || 0

        const { label, color } = getConfidenceLabel(confidence)

        return (
          <div
            key={index}
            className="p-5 bg-white rounded-xl shadow border hover:shadow-md transition"
          >

            {/* 🔹 Header */}
            <div className="flex justify-between items-center mb-3">
              <p className="font-semibold text-lg">
                {item.filename || `Level ${index + 1}`}
              </p>

              <span className={`text-white px-2 py-1 text-xs rounded ${color}`}>
                {label} Confidence
              </span>
            </div>

            {/* 🔹 Difficulty */}
            <p className={`text-xl font-bold ${getDifficultyColor(difficulty)}`}>
              Difficulty: {difficulty.toFixed(2)}
            </p>

            {/* 🔹 Category */}
            <p className="text-sm text-gray-500 mb-2">
              Category: {item.category || "N/A"}
            </p>

            {/* 🔹 Confidence */}
            <p className="text-sm text-gray-600 mb-4">
              Confidence: {(confidence * 100).toFixed(1)}%
            </p>

            {/* 🔹 Explanation */}
            <div className="mb-4">
              <p className="text-sm font-medium mb-1">
                Why this difficulty?
              </p>

              {item.explanation && item.explanation.length > 0 ? (
                item.explanation.map((e: string, i: number) => (
                  <div key={i} className="text-sm text-gray-600">
                    • {e}
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-400">
                  No explanation available
                </p>
              )}
            </div>

            {/* 🔹 Contribution Chart */}
            <ContributionChart contributions={item.contributions} />

            {/* 🔹 Download button */}
            <button
              onClick={() => {
                const blob = new Blob(
                  [JSON.stringify(item, null, 2)],
                  { type: "application/json" }
                )
                const url = URL.createObjectURL(blob)

                const a = document.createElement("a")
                a.href = url
                a.download = `${item.filename || "level"}_analysis.json`
                a.click()
              }}
              className="mt-4 text-sm text-blue-500 hover:underline"
            >
              Download Report
            </button>

          </div>
        )
      })}

    </div>
  )
}