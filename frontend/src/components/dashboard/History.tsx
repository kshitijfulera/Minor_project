"use client"

export default function History({ data = [] }: any) {

  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="mt-10">
        <h3 className="text-xl font-semibold">No history yet</h3>
      </div>
    )
  }

  return (
    <div className="mt-10">
      <h3 className="text-xl font-semibold mb-4">History</h3>

      {data.map((item: any, i: number) => {

        const score =
          typeof item?.difficulty_score === "number"
            ? item.difficulty_score.toFixed(2)
            : "N/A"

        return (
          <div key={i} className="border p-4 rounded mb-2 bg-white shadow">
            <p className="font-medium">{item?.filename || "Unknown"}</p>
            <p className="text-sm text-gray-600">
              Difficulty: {score}
            </p>
          </div>
        )
      })}
    </div>
  )
}