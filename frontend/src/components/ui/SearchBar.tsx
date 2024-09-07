export default function SearchBar() {
  return (
    <div className="max-w-2xl mx-auto mb-8">
      <input
        type="text"
        placeholder="Search..."
        className="w-full px-4 py-2 rounded-md border border-gray-300 bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary"
      />
    </div>
  )
}
