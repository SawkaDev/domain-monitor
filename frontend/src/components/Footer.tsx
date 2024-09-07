export default function Footer() {
  return (
    <footer className="bg-surface py-8">
      <div className="container mx-auto px-4 text-center text-text-secondary">
        <p>&copy; {new Date().getFullYear()} Domain Monitor. All rights reserved.</p>
      </div>
    </footer>
  )
}
