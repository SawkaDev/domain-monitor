import Link from 'next/link'

export default function Logo() {
  return (
    <Link href="/" className="text-2xl font-bold text-text-accent hover:text-text-primary transition-colors">
      Domain Monitor
    </Link>
  )
}
