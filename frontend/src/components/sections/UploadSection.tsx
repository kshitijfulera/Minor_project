"use client"

import { useCallback } from "react"
import { useDropzone } from "react-dropzone"

export default function UploadSection({ refreshData }: any) {

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    try {
      const formData = new FormData()

      // 📦 Add all files
      acceptedFiles.forEach((file) => {
        formData.append("files", file)
      })

      console.log("Uploading files:", acceptedFiles)

      const res = await fetch("http://127.0.0.1:8000/upload-level", {
        method: "POST",
        body: formData
      })

      if (!res.ok) {
        throw new Error("Upload failed")
      }

      const data = await res.json()
      console.log("Upload success:", data)

      // 🔄 Refresh dashboard (IMPORTANT)
      if (typeof refreshData === "function") {
        refreshData()
      }

    } catch (err) {
      console.error("Upload error:", err)
    }
  }, [refreshData])

  // 📥 Drag & Drop
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/json": [".json"]
    }
  })

  return (
    <div className="mb-10">
      <div
        {...getRootProps()}
        className="border-2 border-dashed border-indigo-400 p-10 text-center rounded-xl bg-white shadow hover:shadow-lg transition cursor-pointer"
      >
        <input {...getInputProps()} />

        {isDragActive ? (
          <p className="text-indigo-600 font-medium">
            Drop your JSON files here...
          </p>
        ) : (
          <div>
            <p className="text-lg font-semibold text-gray-700">
              Drag & drop JSON files here
            </p>
            <p className="text-sm text-gray-500 mt-2">
              or click to select files
            </p>
          </div>
        )}
      </div>
    </div>
  )
}