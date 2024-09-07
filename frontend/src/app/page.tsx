export default function Home() {
  return (
    <div className="space-y-12">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-text-primary">Welcome to Domain Monitor</h1>
        <p className="text-xl text-text-secondary max-w-2xl mx-auto">
          View historical domain data and more!
        </p>
      </section>
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {[1, 2, 3].map((item) => (
          <div key={item} className="bg-surface p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-2 text-text-primary">Feature {item}</h2>
            <p className="text-text-secondary">
              Breif Text about the feature. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
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
