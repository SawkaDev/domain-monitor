export default function SearchBar() {
  return (
    <div className="w-full">
      <input
        type="text"
        placeholder="Search..."
        className="w-full px-4 py-2 rounded-full border border-gray-300 bg-white text-text-primary placeholder:text-secondary focus:outline-none focus:ring-2 focus:ring-black"
      />
    </div>
  )
}
