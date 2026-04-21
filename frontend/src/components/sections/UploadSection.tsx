"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { motion } from "framer-motion"
import { UploadCloud } from "lucide-react"
import DifficultyChart from "../DifficultyChart"

export default function UploadSection() {

  const [files, setFiles] = useState<File[]>([])
  const [apiResponse, setApiResponse] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const getColor = (score: number) => {
    if (score > 0.7) return "bg-red-500"
    if (score > 0.4) return "bg-yellow-500"
    return "bg-green-500"
  }

  const onDrop = useCallback(async (acceptedFiles: File[]) => {

    setFiles((prev) => [...prev, ...acceptedFiles])
    setLoading(true)

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

      setApiResponse(data)

    } catch (error) {
      console.error("Error uploading:", error)
    }

    setLoading(false)

  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true
  })

  return (
    <section className="py-24 bg-gradient-to-b from-white to-slate-100">

      <div className="max-w-4xl mx-auto px-6">

        {/* Heading */}
        <h2 className="text-4xl font-bold text-center text-slate-900">
          AI Level Analyzer
        </h2>

        <p className="text-center text-slate-500 mt-3 text-lg">
          Upload game level files and get AI-powered difficulty insights
        </p>

        {/* Upload Box */}
        <div
          {...getRootProps()}
          className="mt-10 border-2 border-dashed border-slate-300 rounded-2xl p-14 text-center cursor-pointer 
          hover:border-indigo-500 hover:bg-indigo-50 transition-all duration-300"
        >
          <input {...getInputProps()} />

          <UploadCloud className="mx-auto mb-4 text-indigo-500" size={40} />

          {isDragActive ? (
            <p className="text-indigo-600 font-medium">
              Drop the files here...
            </p>
          ) : (
            <p className="text-slate-600">
              Drag & drop JSON files here, or click to upload
            </p>
          )}
        </div>

        {/* Empty State */}
        {!apiResponse && !loading && (
          <p className="text-center text-slate-400 mt-10">
            Upload a level file to see AI analysis
          </p>
        )}

        {/* Loading */}
        {loading && (
          <p className="text-center text-indigo-600 mt-6">
            Analyzing level with AI...
          </p>
        )}

        {/* Uploaded Files */}
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

        {/* AI Results */}
        {apiResponse && (
          <div className="mt-10">

            <h3 className="text-xl font-semibold text-slate-900 mb-4">
              AI Analysis Result
            </h3>

            {apiResponse.data.map((item: any, index: number) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="bg-white/80 backdrop-blur-md border border-slate-200 rounded-2xl p-6 mb-6 shadow-lg"
              >

                {/* File */}
                <p className="text-slate-700 mb-2">
                  <strong>File:</strong> {item.filename}
                </p>

                {/* Difficulty Badge */}
                <span className="inline-block px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-700">
                  Difficulty: {item.difficulty_score.toFixed(2)}
                </span>

                {/* Progress Bar */}
                <div className="mt-4">
                  <div className="w-full bg-slate-200 rounded-full h-3">
                    <div
                      className={`${getColor(item.difficulty_score)} h-3 rounded-full`}
                      style={{
                        width: `${item.difficulty_score * 100}%`,
                      }}
                    ></div>
                  </div>
                </div>

                {/* Recommendations */}
                <div className="mt-6">
                  <strong>Recommendations:</strong>

                  {item.recommendations.length > 0 ? (
                    <ul className="space-y-2 mt-3">
                      {item.recommendations.map((rec: string, i: number) => (
                        <li
                          key={i}
                          className="bg-slate-100 px-3 py-2 rounded-lg text-slate-700"
                        >
                          {rec}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-slate-500 mt-2">
                      No major changes needed
                    </p>
                  )}
                </div>

                {/* Chart */}
                <div className="mt-6">
                  <DifficultyChart features={item.features} />
                </div>

              </motion.div>
            ))}

          </div>
        )}

      </div>
    </section>
  )
}