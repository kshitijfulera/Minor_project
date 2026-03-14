"use client"

import { useCallback } from "react"
import { useDropzone, DropzoneOptions } from "react-dropzone"

export default function UploadSection() {

  const onDrop = useCallback((acceptedFiles: File[]) => {
    console.log("Uploaded Files:", acceptedFiles)
  }, [])

  const dropzoneOptions: DropzoneOptions = {
    onDrop,
    multiple: true
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone(dropzoneOptions)

  return (
    <section className="py-24 bg-white">
      <div className="max-w-5xl mx-auto px-6">

        <h2 className="text-3xl font-semibold text-center text-slate-900">
          Upload Game Level Data
        </h2>

        <p className="text-center text-slate-600 mt-4">
          Upload JSON level files or map images for AI difficulty analysis
        </p>

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
              Drag & drop your level files here, or click to upload
            </p>
          )}

        </div>

      </div>
    </section>
  )
}