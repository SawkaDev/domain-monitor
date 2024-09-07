import SearchBar from '../components/ui/SearchBar'

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to Our Website</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover our minimalist approach to design and functionality.
        </p>
      </section>

      <SearchBar />

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {[1, 2, 3].map((item) => (
          <div key={item} className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-2">Feature {item}</h2>
            <p className="text-gray-600">
              A brief description of feature {item}. Keep it concise and impactful.
            </p>
          </div>
        ))}
      </section>

      <section className="text-center">
        <button className="btn-primary">Learn More</button>
      </section>
    </div>
  )
}
