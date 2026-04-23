"use client"

export default function Topbar() {
  return (
    <div className="flex justify-between items-center mb-6">

      <h1 className="text-2xl font-semibold text-slate-800">
        Dashboard
      </h1>

      <div className="flex items-center gap-4">

        <div className="bg-slate-200 w-8 h-8 rounded-full" />

        <span className="text-slate-600">Admin</span>

      </div>

    </div>
  )
}