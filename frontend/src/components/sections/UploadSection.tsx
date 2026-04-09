"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"

export default function UploadSection() {

  const [files, setFiles] = useState<File[]>([])
  const [apiResponse, setApiResponse] = useState<any>(null)

  // onDrop function
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const formData = new FormData()

    acceptedFiles.forEach((file) => {
      formData.append("files", file)
    })

    try {
      const response = await fetch("http://127.0.0.1:8000/upload-level", {
        method: "POST",
        body: formData
      })

      const data = await response.json()

      console.log("API RESPONSE:", data)

      setApiResponse(data)

    } catch (error) {
      console.error("Error uploading:", error)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop
  })

  return (
    <section className="py-24 bg-white">

      <div className="max-w-5xl mx-auto px-6">

        <h2 className="text-3xl font-semibold text-center text-slate-900">
          Upload Game Level Data
        </h2>

        <p className="text-center text-slate-600 mt-4">
          Upload JSON level files or map images for AI difficulty analysis
        </p>

        {/* Upload Box */}

        <div
          {...getRootProps()}
          className="mt-10 border-2 border-dashed border-slate-300 rounded-xl p-12 text-center cursor-pointer hover:border-indigo-500 transition"
        >
          <input {...getInputProps()} />

          {isDragActive ? (
            <p className="text-indigo-600 font-medium">
              Drop the files here...
            </p>
          ) : (
            <p className="text-slate-600">
              Drag & drop JSON or image files here, or click to upload
            </p>
          )}

        </div>

        {/* Uploaded Files */}

        {apiResponse && (
          <div className="mt-10">

            <h3 className="text-xl font-semibold text-slate-900 mb-4">
              AI Analysis Result
            </h3>

            {apiResponse.data.map((item: any, index: number) => (
              <div
                key={index}
                className="border border-slate-200 rounded-lg p-4 mb-4"
              >

                <p className="text-slate-700">
                  <strong>File:</strong> {item.filename}
                </p>

                <p className="text-slate-700">
                  <strong>Difficulty:</strong> {item.difficulty_score.toFixed(2)}
                </p>

                <div className="mt-2">
                  <strong>Recommendations:</strong>
                  <ul className="list-disc ml-6 text-slate-600">
                    {item.recommendations.map((rec: string, i: number) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>

              </div>
            ))}

          </div>
        )}

        {files.length > 0 && (
          <div className="mt-10">

            <h3 className="text-xl font-semibold text-slate-900 mb-4">
              Uploaded Files
            </h3>

            <div className="space-y-3">

              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex justify-between items-center border border-slate-200 rounded-lg p-4"
                >
                  <span className="text-slate-700">{file.name}</span>

                  <span className="text-sm text-slate-500">
                    {(file.size / 1024).toFixed(1)} KB
                  </span>
                </div>
              ))}

            </div>

          </div>
        )}

      </div>

    </section>
  )
}