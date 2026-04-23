"use client"

import { ReactNode } from "react"
import { LayoutDashboard, Upload, BarChart } from "lucide-react"
import Topbar from "./Topbar"   // ✅ make sure this import exists

export default function DashboardLayout({ children }: { children: ReactNode }) {

  return (
    <div className="flex h-screen bg-slate-100">

      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 p-6">

        <h2 className="text-2xl font-bold text-indigo-600 mb-8">
          AI Dashboard
        </h2>

        <nav className="space-y-4">

          <div className="flex items-center gap-3 text-slate-700 hover:text-indigo-600 cursor-pointer">
            <LayoutDashboard size={20} />
            <span>Overview</span>
          </div>

          <div className="flex items-center gap-3 text-slate-700 hover:text-indigo-600 cursor-pointer">
            <Upload size={20} />
            <span>Upload</span>
          </div>

          <div className="flex items-center gap-3 text-slate-700 hover:text-indigo-600 cursor-pointer">
            <BarChart size={20} />
            <span>Analytics</span>
          </div>

        </nav>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 overflow-y-auto p-8">
        <Topbar />
        {children}
      </main>

    </div>
  )
}