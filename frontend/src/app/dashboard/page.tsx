"use client"

import DashboardLayout from "../../components/layout/DashboardLayout"
import UploadSection from "../../components/sections/UploadSection"

export default function DashboardPage() {

    return (
        <DashboardLayout>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 mb-8">

                <div className="bg-white p-6 rounded-xl shadow">
                    <p className="text-slate-500">Total Uploads</p>
                    <h3 className="text-2xl font-bold">12</h3>
                </div>

                <div className="bg-white p-6 rounded-xl shadow">
                    <p className="text-slate-500">Avg Difficulty</p>
                    <h3 className="text-2xl font-bold">0.58</h3>
                </div>

                <div className="bg-white p-6 rounded-xl shadow">
                    <p className="text-slate-500">Last Analysis</p>
                    <h3 className="text-2xl font-bold">Just now</h3>
                </div>

            </div>

            {/* Upload Section */}
            <UploadSection />

        </DashboardLayout>
    )
}