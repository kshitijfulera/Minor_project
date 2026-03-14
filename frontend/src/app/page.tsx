import Hero from "../components/sections/Hero"
import Navbar from "../components/layout/Navbar"
import UploadSection from "../components/sections/UploadSection"
export default function Home() {
  return (
    <main className="min-h-screen bg-white">

      <Navbar />

      <Hero />

      <UploadSection />

    </main>
  )
}