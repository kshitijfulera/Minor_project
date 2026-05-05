export default function Hero() {
  return (
    <section className="py-24 bg-slate-50">
      <div className="max-w-5xl mx-auto px-6 text-center">

        <h1 className="text-5xl font-semibold text-slate-900 leading-tight">
          AI Assisted Game Level Balancing
        </h1>

        <p className="mt-6 text-lg text-slate-600 max-w-2xl mx-auto">
          Upload game level data such as JSON files or map images and let AI
          predict difficulty, failure rate, and provide balancing suggestions.
        </p>

        <div className="mt-10 flex justify-center gap-4">

          <button className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition">
            Upload Level
          </button>

          <button className="border border-slate-300 px-6 py-3 rounded-lg hover:bg-slate-100 transition">
            View Dashboard
          </button>

        </div>

      </div>
    </section>
  )
}