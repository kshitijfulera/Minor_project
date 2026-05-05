export default function Navbar() {
  return (
    <nav className="w-full border-b border-slate-200 bg-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

        <div className="text-3xl font-semibold text-slate-900">
          AI Level Balancer
        </div>

        <div className="flex gap-8 text-slate-600 font-medium">
          <a href="#" className="hover:text-indigo-600">Home</a>
          <a href="#" className="hover:text-indigo-600">Upload</a>
          <a href="#" className="hover:text-indigo-600">Dashboard</a>
          <a href="#" className="hover:text-indigo-600">Docs</a>
        </div>

      </div>
    </nav>
  )
}