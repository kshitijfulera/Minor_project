"use client"

export default function RecentActivity() {

  const mock = [
    "Uploaded level1.json",
    "Analyzed difficulty 0.62",
    "Generated recommendations",
  ]

  return (
    <div className="bg-white p-6 rounded-xl shadow mt-6">

      <h3 className="text-lg font-semibold mb-4">
        Recent Activity
      </h3>

      <ul className="space-y-2 text-slate-600">
        {mock.map((item, i) => (
          <li key={i}>• {item}</li>
        ))}
      </ul>

    </div>
  )
}